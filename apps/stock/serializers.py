from rest_framework import serializers

from apps.material.models import Material
from apps.product.models import Product
from .models import StockLevel, InventoryMovementLog


class StockLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLevel
        fields = [
            "id",
            "material",
            "product",
            "location",
            "quantity",
        ]


class InventoryMovementLogSerializer(serializers.ModelSerializer):
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), required=False, allow_null=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, allow_null=True)

    class Meta:
        model = InventoryMovementLog
        fields = [
            "id",
            "material",
            "product",
            "from_location",
            "to_location",
            "quantity",
            "created_at",
            "user",
        ]

    def get_fields(self):
        fields = super().get_fields()
        # Check if initial_data is available (not available during schema generation)
        if hasattr(self, 'initial_data') and self.initial_data:
            from_location = self.initial_data.get('from_location')
            if from_location:
                # Get available materials
                material_ids = StockLevel.objects.filter(location_id=from_location, material__isnull=False, quantity__gt=0).values_list('material', flat=True)
                fields['material'].queryset = Material.objects.filter(id__in=material_ids)
                
                # Get available products
                product_ids = StockLevel.objects.filter(location_id=from_location, product__isnull=False, quantity__gt=0).values_list('product', flat=True)
                fields['product'].queryset = Product.objects.filter(id__in=product_ids)
            else:
                fields['material'].queryset = Material.objects.none()
                fields['product'].queryset = Product.objects.none()
        else:
            # During schema generation, use all materials and products
            fields['material'].queryset = Material.objects.all()
            fields['product'].queryset = Product.objects.all()
        return fields

    def validate(self, attrs):
        from_location = attrs.get('from_location')
        material = attrs.get('material')
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        
        # Check that either material or product is selected, but not both
        if material is None and product is None:
            raise serializers.ValidationError("Material yoki Product tanlanishi kerak!")
        if material is not None and product is not None:
            raise serializers.ValidationError("Material va Product bir vaqtda tanlanishi mumkin emas!")
        
        # Check stock availability
        if from_location:
            if material:
                stock = StockLevel.objects.filter(location=from_location, material=material).first()
                if not stock or stock.quantity <= 0:
                    raise serializers.ValidationError(f"'{material.name}' materiali '{from_location}' locationida mavjud emas!")
                if quantity > stock.quantity:
                    raise serializers.ValidationError(f"'{from_location}' locationida {stock.quantity} dan ko'p '{material.name}' materiali yo'q!")
            elif product:
                stock = StockLevel.objects.filter(location=from_location, product=product).first()
                if not stock or stock.quantity <= 0:
                    raise serializers.ValidationError(f"'{product.name}' mahsuloti '{from_location}' locationida mavjud emas!")
                if quantity > stock.quantity:
                    raise serializers.ValidationError(f"'{from_location}' locationida {stock.quantity} dan ko'p '{product.name}' mahsuloti yo'q!")
        
        return attrs