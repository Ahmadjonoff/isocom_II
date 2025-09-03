from django.db import models
from apps.material.models import BaseModel

class WorkCenter(BaseModel):
    TYPE_CHOICES = (
        ("EXTRUDER", "Extruder"),
        ("DEGASSING_AREA", "Degassing Area"),
        ("LAMINATOR", "Laminator"),
        ("BRONIROVSHIK", "Bronirovshik"),
        ("DUPLICATOR", "Duplicator"),
        ("PACKAGING", "Packaging"),
        ("QUALITY_CONTROL", "Quality Control"),
        ("BRAK_MAYDALAGICH", "Brak maydalagich"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    location = models.ForeignKey('warehouse.Location', on_delete=models.SET_NULL, null=True, blank=True)
    capacity_per_hour = models.IntegerField(null=True, blank=True)
    capacity_unit = models.CharField(max_length=20, null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


