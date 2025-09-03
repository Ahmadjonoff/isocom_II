import uuid
from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Material(BaseModel):
    TYPE_CHOICES = (
        ("GRANULA", "Granula"),
        ("ZAR", "Zar"),
        ("OTHER", "Other"),
    )

    UNIT_OF_MEASURE_CHOICES = (
        ("KG", "kg"),
        ("METER", "m"),
        ("METER_SQUARE", "m²"),
        ("METER_CUBIC", "m³"),
        ("PIECE", "piece"),
        ("LITER", "l"),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    unit_of_measure = models.CharField(max_length=12, choices=UNIT_OF_MEASURE_CHOICES, default="KG")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="GRANULA")
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"