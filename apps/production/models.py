from django.core.exceptions import ValidationError
from django.db import models, transaction
from apps.stock.models import StockLevel
from apps.warehouse.models import Location
from apps.workcenter.models import WorkCenter
from apps.material.models import BaseModel

UNIT_OF_MEASURE_CHOICES = (
        ("KG", "kg"),
        ("METER", "m"),
        ("METER_SQUARE", "m²"),
        ("METER_CUBIC", "m³"),
        ("PIECE", "piece"),
        ("LITER", "l"),
    )


class ProductionStep(BaseModel):
    """Manufacturing workflow steps"""
    STEP_TYPE_CHOICES = (
        ("EXTRUSION", "Extrusion"),
        ("DEGASSING", "Degassing (10 kun)"),
        ("LAMINATION", "Lamination"),
        ("BRONZING", "Bronzing"),
        ("DUPLICATION", "Duplication"),
        ("PACKAGING", "Packaging"),
        ("QUALITY_CONTROL", "Quality Control"),
        ("WAREHOUSE_TRANSFER", "Warehouse Transfer"),
        ("CUSTOMER_DELIVERY", "Customer Delivery"),
    )
    
    name = models.CharField(max_length=100)
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Step duration in hours")
    is_required = models.BooleanField(default=True)
    order_sequence = models.PositiveIntegerField(default=0, help_text="Order of execution")
    
    class Meta:
        ordering = ['order_sequence']
    
    def __str__(self):
        return f"{self.name} ({self.get_step_type_display()})"


class Order(BaseModel):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    produced_product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name="produced_by")
    unit_of_measure = models.CharField(max_length=12, choices=UNIT_OF_MEASURE_CHOICES, default="KG")
    produced_quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Production quantity")
    operators = models.ManyToManyField('user.User', blank=True, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        product_name = self.produced_product.name if self.produced_product else "Unknown Product"
        return f"Order {self.id} - {product_name} ({self.produced_quantity})"
    
    def create_production_steps(self):
        """Create default production steps for this order"""
        default_steps = [
            ("EXTRUSION", "Extrusion", 1, 8.0),
            ("DEGASSING", "Degassing (10 kun)", 2, 240.0),  # 10 days = 240 hours
            ("LAMINATION", "Lamination", 3, 4.0),
            ("BRONZING", "Bronzing", 4, 2.0),
            ("DUPLICATION", "Duplication", 5, 2.0),
            ("PACKAGING", "Packaging", 6, 1.0),
            ("QUALITY_CONTROL", "Quality Control", 7, 0.5),
            ("WAREHOUSE_TRANSFER", "Warehouse Transfer", 8, 0.5),
        ]
        
        for step_type, name, sequence, duration in default_steps:
            step, created = ProductionStep.objects.get_or_create(
                step_type=step_type,
                defaults={
                    'name': name,
                    'order_sequence': sequence,
                    'duration_hours': duration,
                    'is_required': True
                }
            )
            
            # Create execution record for this order
            ProductionStepExecution.objects.get_or_create(
                order=self,
                production_step=step,
                defaults={'status': 'PENDING'}
            )
    
    def get_current_step(self):
        """Get the current step in progress or next pending step"""
        return self.step_executions.filter(
            status__in=['IN_PROGRESS', 'PENDING']
        ).order_by('production_step__order_sequence').first()
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on completed steps"""
        total_steps = self.step_executions.count()
        if total_steps == 0:
            return 0
        completed_steps = self.step_executions.filter(status='COMPLETED').count()
        return (completed_steps / total_steps) * 100


class ProductionStepExecution(BaseModel):
    """Tracks execution of production steps for orders"""
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("SKIPPED", "Skipped"),
        ("FAILED", "Failed"),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="step_executions")
    production_step = models.ForeignKey(ProductionStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    assigned_operator = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    actual_duration_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    quality_notes = models.TextField(null=True, blank=True, help_text="Quality control notes")
    quantity_processed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['production_step__order_sequence']
        unique_together = ['order', 'production_step']
    
    def __str__(self):
        return f"{self.order} - {self.production_step.name} ({self.get_status_display()})"
    
    def clean(self):
        super().clean()
        if self.status == "COMPLETED" and not self.end_time:
            raise ValidationError("Completed steps must have an end time")
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")


class UsedMaterial(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="used_materials")
    material = models.ForeignKey('material.Material', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Kg")
    step_execution = models.ForeignKey(ProductionStepExecution, on_delete=models.SET_NULL, null=True, blank=True, related_name="materials_used")

    def __str__(self):
        return f"{self.material.name} - {self.quantity}kg used"

    def _get_workcenter_location(self):
        """Get workcenter location based on step_execution work_center, fallback to order work_center"""
        # First try to get workcenter from step_execution
        if self.step_execution and self.step_execution.work_center:
            wc = self.step_execution.work_center
        # Fallback to order work_center
        elif self.order and self.order.work_center:
            wc = self.order.work_center
        else:
            return None
            
        return Location.objects.filter(work_center=wc, location_type="WORKCENTER").first()

    def _check_material_availability(self, location):
        """Check if material is available in the specified location"""
        try:
            stock_level = StockLevel.objects.get(material=self.material, location=location)
            available_quantity = stock_level.quantity
        except StockLevel.DoesNotExist:
            available_quantity = 0
        
        if available_quantity < self.quantity:
            workcenter_name = location.work_center.name if location.work_center else "Noma'lum"
            raise ValidationError(
                f"'{self.material.name}' materiali '{workcenter_name}' stanokida yetarli miqdorda mavjud emas! "
                f"Mavjud: {available_quantity} kg, Kerak: {self.quantity} kg"
            )

    def clean(self):
        super().clean()
        # Basic validation - detailed validation is done in save() method
        if not self.material:
            raise ValidationError("Material tanlanishi kerak!")
        if not self.quantity or self.quantity <= 0:
            raise ValidationError("Miqdor 0 dan katta bo'lishi kerak!")
        if not self.order:
            raise ValidationError("Order tanlanishi kerak!")

    def save(self, *args, **kwargs):
        is_create = self._state.adding
        
        with transaction.atomic():
            # Run basic validation first
            self.clean()
            
            # Get workcenter location once and validate
            wc_loc = self._get_workcenter_location()
            if not wc_loc:
                if self.step_execution and not self.step_execution.work_center:
                    raise ValidationError("Step execution work_center topilmadi. Avval step execution uchun work_center tayinlang.")
                elif not self.order or not self.order.work_center:
                    raise ValidationError("Order work_center topilmadi. Avval order uchun work_center tayinlang.")
                else:
                    raise ValidationError("Workcenter location topilmadi. Avval workcenter uchun WORKCENTER lokatsiyasini yarating.")
            
            # Check material availability for new records
            if is_create:
                self._check_material_availability(wc_loc)
            
            # Save the record
            super().save(*args, **kwargs)
            
            # Adjust stock for new records
            if is_create:
                StockLevel.adjust_material(self.material, wc_loc, -self.quantity)

    def delete(self, *args, **kwargs):
        wc_loc = self._get_workcenter_location()
        with transaction.atomic():
            if wc_loc is not None:
                StockLevel.adjust_material(self.material, wc_loc, self.quantity)
            return super().delete(*args, **kwargs)


class ProductionOutput(BaseModel):
    """Tracks products produced at each step"""
    step_execution = models.ForeignKey(ProductionStepExecution, on_delete=models.CASCADE, related_name="outputs")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    unit_of_measure = models.CharField(max_length=12, choices=UNIT_OF_MEASURE_CHOICES, default="KG")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text="og'irlik")
    quality_status = models.CharField(max_length=20, choices=[
        ("PASSED", "Passed"),
        ("FAILED", "Failed"),
        ("PENDING", "Pending"),
    ], default="PENDING")
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.get_unit_of_measure_display()} ({self.get_quality_status_display()})"