from django.db import models
from apps.material.models import BaseModel


class Product(BaseModel):
    TYPE_CHOICES = (
        ("FINISHED_PRODUCT", "Tayyor mahsulot"),
        ("SEMI_FINISHED_PRODUCT", "Yarim tayyor mahsulot"),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="FINISHED_PRODUCT")
    photo = models.ImageField(upload_to="product_photos/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, help_text="Uzunlik (m)")
    thickness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Qalinlik (sm)")
    diameter = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Diametr (sm)")
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Kenglik (sm)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class ProductComponent(BaseModel):
    finished_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="components")
    semi_finished_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="used_in", null=True, blank=True)

    def __str__(self):
        return f"{self.semi_finished_product.name} in {self.finished_product.name}"