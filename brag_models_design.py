"""
Brag (Scrap) Management System Models Design
TZ M4, M7, M8 modullariga muvofiq
"""

from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from apps.material.models import BaseModel

# ============================================================================
# 1. BRAG GENERATION (Har bir step da brag hosil bo'lishi)
# ============================================================================

class ScrapGeneration(BaseModel):
    """
    Har bir production step da hosil bo'lgan brag
    TZ M4: Mass-balans asosida hisobiy brag
    """
    SCRAP_TYPE_CHOICES = (
        ("CALCULATED", "Hisobiy (Input-Output)"),     # Extruder, Bronirovshik
        ("FIXED_PER_UNIT", "Birlik uchun fixed"),     # Laminator (jadval bo'yicha)
        ("MEASURED", "O'lchangan"),                   # Boshqa holatlar
    )
    
    SOURCE_TYPE_CHOICES = (
        ("EXTRUDER", "Extruder"),
        ("BRONIROVSHIK", "Bronirovshik (E3)"),
        ("LAMINATOR", "Laminator"),
        ("DUPLICATOR", "Duplicator"), 
        ("PACKAGING", "Packaging"),
        ("QUALITY_CONTROL", "Quality Control"),
        ("OTHER", "Other"),
    )
    
    DRABILKA_TYPE_CHOICES = (
        ("HARD", "Hard Drabilka"),
        ("SOFT", "Yumshoq Drabilka"),
    )
    
    # Links
    step_execution = models.ForeignKey(
        'production.ProductionStepExecution', 
        on_delete=models.CASCADE, 
        related_name='generated_scraps'
    )
    
    # Brag details
    scrap_type = models.CharField(max_length=20, choices=SCRAP_TYPE_CHOICES)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    
    # Hisobiy brag (calculated)
    input_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    output_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    wip_kg = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    calculated_scrap_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    
    # Fixed brag (laminator)
    units_produced = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scrap_per_unit_kg = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    fixed_scrap_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    
    # Final brag amount
    total_scrap_kg = models.DecimalField(max_digits=12, decimal_places=3)
    drabilka_type = models.CharField(max_length=10, choices=DRABILKA_TYPE_CHOICES)
    
    # Status
    is_collected = models.BooleanField(default=False)
    collection_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_source_type_display()} Brag: {self.total_scrap_kg}kg ({self.get_scrap_type_display()})"
    
    def clean(self):
        super().clean()
        
        if self.scrap_type == "CALCULATED":
            if not all([self.input_kg, self.output_kg]):
                raise ValidationError("Calculated scrap uchun input_kg va output_kg kerak!")
            self.calculated_scrap_kg = self.input_kg - self.output_kg - self.wip_kg
            self.total_scrap_kg = self.calculated_scrap_kg
            
        elif self.scrap_type == "FIXED_PER_UNIT":
            if not all([self.units_produced, self.scrap_per_unit_kg]):
                raise ValidationError("Fixed scrap uchun units_produced va scrap_per_unit_kg kerak!")
            self.fixed_scrap_kg = self.units_produced * self.scrap_per_unit_kg
            self.total_scrap_kg = self.fixed_scrap_kg
            
        # Set drabilka type based on source
        if self.source_type in ["EXTRUDER", "BRONIROVSHIK"]:
            self.drabilka_type = "HARD"
        else:
            self.drabilka_type = "SOFT"
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# ============================================================================
# 2. SCRAP BATCH (Drabilka uchun to'plangan braglar)
# ============================================================================

class ScrapBatch(BaseModel):
    """
    Drabilka uchun to'plangan brag partiyasi
    TZ M8: Rework IN jarayoni
    """
    BATCH_TYPE_CHOICES = (
        ("HARD", "Hard Drabilka"),
        ("SOFT", "Yumshoq Drabilka"),
    )
    
    batch_number = models.CharField(max_length=50, unique=True)
    batch_type = models.CharField(max_length=10, choices=BATCH_TYPE_CHOICES)
    
    # Collection details
    collected_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    collection_date = models.DateTimeField(auto_now_add=True)
    
    # Weight tracking
    expected_weight_kg = models.DecimalField(max_digits=12, decimal_places=3)
    actual_weight_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    weight_difference_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ("COLLECTING", "To'planmoqda"),
        ("READY_FOR_REWORK", "Qayta ishlashga tayyor"),
        ("IN_REWORK", "Qayta ishlanmoqda"),
        ("COMPLETED", "Yakunlangan"),
    ], default="COLLECTING")
    
    # Rework reference
    rework_order = models.ForeignKey(
        'ReworkOrder', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='source_batches'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Batch {self.batch_number} ({self.get_batch_type_display()}) - {self.expected_weight_kg}kg"
    
    def add_scrap(self, scrap_generation):
        """Add scrap to this batch"""
        if scrap_generation.drabilka_type.upper() != self.batch_type:
            raise ValidationError(f"Scrap type mismatch: {scrap_generation.drabilka_type} != {self.batch_type}")
        
        ScrapBatchItem.objects.create(
            batch=self,
            scrap_generation=scrap_generation
        )
        
        # Update expected weight
        self.expected_weight_kg += scrap_generation.total_scrap_kg
        self.save(update_fields=['expected_weight_kg'])
        
        # Mark scrap as collected
        scrap_generation.is_collected = True
        scrap_generation.collection_date = self.collection_date
        scrap_generation.save(update_fields=['is_collected', 'collection_date'])
    
    def calculate_weight_difference(self):
        """Calculate difference between expected and actual weight"""
        if self.actual_weight_kg is not None:
            self.weight_difference_kg = self.actual_weight_kg - self.expected_weight_kg
            self.save(update_fields=['weight_difference_kg'])
            return self.weight_difference_kg
        return None


class ScrapBatchItem(BaseModel):
    """
    ScrapBatch ichidagi individual scrap items
    """
    batch = models.ForeignKey(ScrapBatch, on_delete=models.CASCADE, related_name='items')
    scrap_generation = models.OneToOneField(ScrapGeneration, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['batch', 'scrap_generation']
    
    def __str__(self):
        return f"{self.batch.batch_number} - {self.scrap_generation}"


# ============================================================================
# 3. REWORK ORDER & VT PRODUCTION (Drabilka jarayoni)
# ============================================================================

class ReworkOrder(BaseModel):
    """
    Drabilka buyurtmasi - bragni VT ga aylantirish
    TZ M8: Rework/VT workflow
    """
    STATUS_CHOICES = (
        ("PLANNED", "Rejalashtirilgan"),
        ("IN_PROGRESS", "Jarayonda"),
        ("COMPLETED", "Yakunlangan"),
        ("CANCELLED", "Bekor qilingan"),
    )
    
    order_number = models.CharField(max_length=50, unique=True)
    rework_type = models.CharField(max_length=10, choices=[
        ("HARD", "Hard → Soft"),
        ("SOFT", "Soft → VT"),
        ("COMBINED", "Hard → Soft → VT"),
    ])
    
    # Operator
    operator = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    
    # Planning
    planned_date = models.DateField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNED")
    
    # Notes
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rework {self.order_number} ({self.get_rework_type_display()})"


class ReworkProcess(BaseModel):
    """
    Rework jarayoni - IN va OUT tracking
    TZ M8: ReworkIO equivalent
    """
    rework_order = models.ForeignKey(ReworkOrder, on_delete=models.CASCADE, related_name='processes')
    
    # Input tracking
    input_batch = models.ForeignKey(ScrapBatch, on_delete=models.CASCADE, related_name='rework_processes')
    input_weight_kg = models.DecimalField(max_digits=12, decimal_places=3)
    input_timestamp = models.DateTimeField()
    input_device = models.ForeignKey('Device', on_delete=models.SET_NULL, null=True, blank=True)  # Scale device
    
    # Output tracking  
    output_weight_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    output_timestamp = models.DateTimeField(null=True, blank=True)
    output_device = models.ForeignKey('Device', on_delete=models.SET_NULL, null=True, blank=True, related_name='rework_outputs')
    
    # Loss calculation
    loss_kg = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    loss_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rework Process: {self.input_weight_kg}kg → {self.output_weight_kg or '?'}kg"
    
    def calculate_loss(self):
        """Calculate loss when output is recorded"""
        if self.output_weight_kg is not None:
            self.loss_kg = self.input_weight_kg - self.output_weight_kg
            if self.input_weight_kg > 0:
                self.loss_percentage = (self.loss_kg / self.input_weight_kg) * 100
            self.save(update_fields=['loss_kg', 'loss_percentage'])


# ============================================================================
# 4. VT BATCH (Ishlab chiqarilgan vtorichka)
# ============================================================================

class VTBatch(BaseModel):
    """
    Vtorichka (secondary material) partiyasi
    TZ M8: VT Main omborga kirim
    """
    batch_number = models.CharField(max_length=50, unique=True)
    rework_process = models.ForeignKey(ReworkProcess, on_delete=models.CASCADE, related_name='vt_batches')
    
    # Material info
    vt_material = models.ForeignKey('material.Material', on_delete=models.CASCADE)  # VT material
    weight_kg = models.DecimalField(max_digits=12, decimal_places=3)
    
    # Quality
    quality_grade = models.CharField(max_length=10, choices=[
        ("A", "A grade"),
        ("B", "B grade"), 
        ("C", "C grade"),
    ], default="B")
    
    # Transfer to stock
    is_transferred_to_stock = models.BooleanField(default=False)
    transfer_date = models.DateTimeField(null=True, blank=True)
    stock_location = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"VT Batch {self.batch_number} - {self.weight_kg}kg ({self.vt_material.name})"
    
    def transfer_to_main_stock(self):
        """Transfer VT to main warehouse stock"""
        from apps.stock.models import StockLevel
        from apps.warehouse.models import Location
        
        # Get main warehouse location
        main_location = Location.objects.filter(location_type="WAREHOUSE").first()
        if not main_location:
            raise ValidationError("Main warehouse location not found!")
        
        # Adjust stock level
        StockLevel.adjust_material(self.vt_material, main_location, self.weight_kg)
        
        # Update transfer status
        self.is_transferred_to_stock = True
        self.transfer_date = timezone.now()
        self.stock_location = main_location
        self.save(update_fields=['is_transferred_to_stock', 'transfer_date', 'stock_location'])


# ============================================================================
# 5. LAMINATOR SCRAP CONFIG (Rasmdagi jadval)
# ============================================================================

class LaminatorScrapConfig(BaseModel):
    """
    Laminator uchun mahsulot turiga qarab fixed scrap miqdorlari
    Rasmdagi jadval ma'lumotlari
    """
    product_code = models.CharField(max_length=10, unique=True)  # p5, p4, p3, p2
    thickness_mm = models.DecimalField(max_digits=5, decimal_places=2)
    width_cm = models.DecimalField(max_digits=6, decimal_places=2) 
    length_m = models.DecimalField(max_digits=8, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=3)
    shpulya_kg = models.DecimalField(max_digits=6, decimal_places=3)
    net_product_kg = models.DecimalField(max_digits=8, decimal_places=3)
    scrap_per_roll_kg = models.DecimalField(max_digits=6, decimal_places=3)
    
    # Calculated fields
    scrap_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['product_code']
    
    def __str__(self):
        return f"{self.product_code}: {self.scrap_per_roll_kg}kg brag/rulon"
    
    def save(self, *args, **kwargs):
        # Calculate scrap percentage
        if self.weight_kg > 0:
            self.scrap_percentage = (self.scrap_per_roll_kg / self.weight_kg) * 100
        super().save(*args, **kwargs)


# ============================================================================
# 6. DEVICE MODEL (Scale devices uchun)
# ============================================================================

class Device(BaseModel):
    """
    Scale va boshqa o'lchov qurilmalari
    TZ M15: IoT/RS pipeline
    """
    DEVICE_TYPE_CHOICES = (
        ("SCALE", "Scale/Tarozi"),
        ("LENGTH_COUNTER", "Length Counter"),
        ("TEMPERATURE", "Temperature Sensor"),
    )
    
    device_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    
    # Location
    work_center = models.ForeignKey('workcenter.WorkCenter', on_delete=models.SET_NULL, null=True, blank=True)
    location_description = models.CharField(max_length=200, null=True, blank=True)
    
    # Calibration
    last_calibration_date = models.DateTimeField(null=True, blank=True)
    calibration_due_date = models.DateTimeField(null=True, blank=True)
    calibration_certificate = models.CharField(max_length=100, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['device_id']
    
    def __str__(self):
        return f"{self.device_id} ({self.get_device_type_display()})"
    
    @property
    def is_calibration_valid(self):
        """Check if calibration is still valid"""
        if not self.calibration_due_date:
            return False
        from django.utils import timezone
        return timezone.now() < self.calibration_due_date
