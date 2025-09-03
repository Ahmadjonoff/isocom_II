from rest_framework import serializers
from .models import Warehouse, Location


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "location_type",
            "warehouse",
            "work_center",
            "is_active",
            "created_at",
            "updated_at",
        ]


