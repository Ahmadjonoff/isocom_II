from django.db import models, transaction
from django.core.exceptions import ValidationError
from apps.material.models import BaseModel



class StockLevel(BaseModel):
    material = models.ForeignKey('material.Material', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey('warehouse.Location', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=16, decimal_places=3, default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name="stocklevel_quantity_gte_0"),
            models.CheckConstraint(
                check=~(models.Q(material__isnull=True) & models.Q(product__isnull=True)),
                name="stocklevel_material_or_product_present",
            ),
            models.CheckConstraint(
                check=~(models.Q(material__isnull=False) & models.Q(product__isnull=False)),
                name="stocklevel_material_or_product_not_both",
            ),
            models.UniqueConstraint(fields=["material", "location"], name="uq_stocklevel_material_location"),
            models.UniqueConstraint(fields=["product", "location"], name="uq_stocklevel_product_location"),
        ]
        indexes = [
            models.Index(fields=["material", "location"], name="ix_stk_mat_loc"),
            models.Index(fields=["product", "location"], name="ix_stk_prod_loc"),
        ]

    def __str__(self):
        if self.material:
            return f"{self.material.name} @ {self.location} = {self.quantity}"
        elif self.product:
            return f"{self.product.name} @ {self.location} = {self.quantity}"
        return f"Unknown @ {self.location} = {self.quantity}"

    def clean(self):
        super().clean()
        if self.material is None and self.product is None:
            raise ValidationError("Material yoki Product tanlanishi kerak!")
        if self.material is not None and self.product is not None:
            raise ValidationError("Material va Product bir vaqtda tanlanishi mumkin emas!")
        if self.location and getattr(self.location, "location_type", None) == "WORKSHOP":
            raise ValidationError("StockLevel faqat 'Warehouse' va 'Workcenter stage' turidagi location uchun ruxsat etiladi!")

    def save(self, *args, **kwargs):
        # Ensure business rules are enforced even when created programmatically
        self.clean()
        return super().save(*args, **kwargs)

    @classmethod
    def adjust_material(cls, material, location, delta_quantity):
        if location is None or material is None or delta_quantity == 0:
            return
        if getattr(location, "location_type", None) == "WORKSHOP":
            raise ValidationError(f"'{location}' locationi 'Warehouse' va 'Workcenter stage' turidagi location emas. StockLevel faqat Warehouse va Workcenter stage uchun ruxsat etiladi!")
        with transaction.atomic():
            try:
                obj = cls.objects.select_for_update().get(material=material, location=location)
            except cls.DoesNotExist:
                if delta_quantity < 0:
                    raise ValidationError(f"'{material.name}' materiali '{location}' locationida mavjud emas!")
                obj = cls.objects.create(material=material, location=location, quantity=0)
            
            new_qty = obj.quantity + delta_quantity
            if new_qty < 0:
                raise ValidationError(f"'{material.name}' materiali '{location}' locationida yetarli miqdorda mavjud emas! Mavjud: {obj.quantity}, Kerak: {abs(delta_quantity)}")
            
            obj.quantity = new_qty
            obj.save(update_fields=["quantity"])

    @classmethod
    def adjust_product(cls, product, location, delta_quantity):
        if location is None or product is None or delta_quantity == 0:
            return
        if getattr(location, "location_type", None) == "WORKSHOP":
            raise ValidationError(f"'{location}' locationi 'Warehouse' va 'Workcenter stage' turidagi location emas. StockLevel faqat Warehouse va Workcenter stage uchun ruxsat etiladi!")
        with transaction.atomic():
            try:
                obj = cls.objects.select_for_update().get(product=product, location=location)
            except cls.DoesNotExist:
                if delta_quantity < 0:
                    raise ValidationError(f"'{product.name}' mahsuloti '{location}' locationida mavjud emas!")
                obj = cls.objects.create(product=product, location=location, quantity=0)
            
            new_qty = obj.quantity + delta_quantity
            if new_qty < 0:
                raise ValidationError(f"'{product.name}' mahsuloti '{location}' locationida yetarli miqdorda mavjud emas! Mavjud: {obj.quantity}, Kerak: {abs(delta_quantity)}")
            
            obj.quantity = new_qty
            obj.save(update_fields=["quantity"])


class InventoryMovementLog(BaseModel):
    material = models.ForeignKey('material.Material', on_delete=models.CASCADE, related_name='inventory_material_logs', null=True, blank=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='inventory_product_logs', null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    from_location = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='outgoing_inventory_logs')
    to_location = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_inventory_logs')
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name="inventorylog_quantity_gt_0"),
            models.CheckConstraint(
                check=~(models.Q(from_location__isnull=True) & models.Q(to_location__isnull=True)),
                name="inventorylog_from_or_to_present",
            ),
            models.CheckConstraint(
                check=~(models.Q(material__isnull=True) & models.Q(product__isnull=True)),
                name="inventorylog_material_or_product_present",
            ),
            models.CheckConstraint(
                check=~(models.Q(material__isnull=False) & models.Q(product__isnull=False)),
                name="inventorylog_material_or_product_not_both",
            ),
        ]

    def __str__(self):
        direction = "Transfer"
        if self.from_location is None:
            direction = "IN"
        elif self.to_location is None:
            direction = "OUT"
        
        if self.material:
            item_name = self.material.name
            uom = self.material.unit_of_measure
        elif self.product:
            item_name = self.product.name
            uom = ""
        else:
            item_name = "(no item)"
            uom = ""
        
        return f"{direction} - {item_name} - {self.quantity} {uom}".strip()

    def clean(self):
        super().clean()
        if self.material is None and self.product is None:
            raise ValidationError("Material yoki Product tanlanishi kerak!")
        if self.material is not None and self.product is not None:
            raise ValidationError("Material va Product bir vaqtda tanlanishi mumkin emas!")
        
        # Check stock availability
        if self.from_location:
            if self.material:
                stock = StockLevel.objects.filter(location=self.from_location, material=self.material).first()
                if not stock or stock.quantity < self.quantity:
                    raise ValidationError(f"'{self.material.name}' materiali '{self.from_location}' locationida yetarli miqdorda mavjud emas!")
            elif self.product:
                stock = StockLevel.objects.filter(location=self.from_location, product=self.product).first()
                if not stock or stock.quantity < self.quantity:
                    raise ValidationError(f"'{self.product.name}' mahsuloti '{self.from_location}' locationida yetarli miqdorda mavjud emas!")

    def save(self, *args, **kwargs):
        self.clean()
        # Check if this is a new record by checking if we have a pk
        is_create = not hasattr(self, '_state') or self._state.adding
        
        # Get old values for update
        old_quantity = None
        old_from_location = None
        old_to_location = None
        old_material = None
        old_product = None
        
        if not is_create and self.pk:
            try:
                old_instance = InventoryMovementLog.objects.get(pk=self.pk)
                old_quantity = old_instance.quantity
                old_from_location = old_instance.from_location
                old_to_location = old_instance.to_location
                old_material = old_instance.material
                old_product = old_instance.product
            except InventoryMovementLog.DoesNotExist:
                pass
        
        with transaction.atomic():
            super().save(*args, **kwargs)
            
            if is_create:
                # New record - adjust stock levels
                if self.material is not None:
                    if self.from_location is not None:
                        StockLevel.adjust_material(self.material, self.from_location, -self.quantity)
                    if self.to_location is not None:
                        StockLevel.adjust_material(self.material, self.to_location, self.quantity)
                elif self.product is not None:
                    if self.from_location is not None:
                        StockLevel.adjust_product(self.product, self.from_location, -self.quantity)
                    if self.to_location is not None:
                        StockLevel.adjust_product(self.product, self.to_location, self.quantity)
            else:
                # Update record - reverse old changes and apply new changes
                if old_quantity is not None:
                    # Reverse old changes
                    if old_material is not None:
                        if old_from_location is not None:
                            StockLevel.adjust_material(old_material, old_from_location, old_quantity)
                        if old_to_location is not None:
                            StockLevel.adjust_material(old_material, old_to_location, -old_quantity)
                    elif old_product is not None:
                        if old_from_location is not None:
                            StockLevel.adjust_product(old_product, old_from_location, old_quantity)
                        if old_to_location is not None:
                            StockLevel.adjust_product(old_product, old_to_location, -old_quantity)
                    
                    # Apply new changes
                    if self.material is not None:
                        if self.from_location is not None:
                            StockLevel.adjust_material(self.material, self.from_location, -self.quantity)
                        if self.to_location is not None:
                            StockLevel.adjust_material(self.material, self.to_location, self.quantity)
                    elif self.product is not None:
                        if self.from_location is not None:
                            StockLevel.adjust_product(self.product, self.from_location, -self.quantity)
                        if self.to_location is not None:
                            StockLevel.adjust_product(self.product, self.to_location, self.quantity)