from rest_framework import serializers
from .models import Product, ProductComponent


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "code",
            "description",
            "price",
            "type",
            "is_active",
            "created_at",
            "updated_at",
        ]

class ProductComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComponent
        fields = [
            "id",
            "finished_product",
            "semi_finished_product",
            "created_at",
            "updated_at",
        ]