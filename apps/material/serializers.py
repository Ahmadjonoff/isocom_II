from rest_framework import serializers
from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "slug",
            "code",
            "unit_of_measure",
            "type",
            "description",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]


