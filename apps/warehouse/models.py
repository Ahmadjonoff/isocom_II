from django.db import models
from django.db.models import Q
from apps.material.models import BaseModel

class Warehouse(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Location(BaseModel):
    LOCATION_TYPE_CHOICES = (
        ("WAREHOUSE", "Warehouse"),
        ("WORKCENTER", "Work Center Staging"),
        ("WORKSHOP", "Workshop"),
    )

    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True, related_name="locations")
    work_center = models.ForeignKey('workcenter.WorkCenter', on_delete=models.CASCADE, null=True, blank=True, related_name="locations")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(location_type="WAREHOUSE", warehouse__isnull=False, work_center__isnull=True)
                    |
                    Q(location_type="WORKCENTER", warehouse__isnull=True, work_center__isnull=False)
                    |
                    Q(location_type="WORKSHOP", warehouse__isnull=True, work_center__isnull=True)
                ),
                name="location_type_matches_reference",
            ),
        ]

    def __str__(self):
        suffix = self.warehouse.name if self.warehouse else (self.work_center.name if self.work_center else "")
        return f"{self.name} ({self.get_location_type_display()} {suffix})".strip()