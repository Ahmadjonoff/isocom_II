from rest_framework import serializers
from .models import WorkCenter


class WorkCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCenter
        fields = [
            "id",
            "name",
            "description",
            "type",
            "location",
            "capacity_per_hour",
            "capacity_unit",
            "last_maintenance_date",
            "is_active",
        ]


