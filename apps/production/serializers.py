from rest_framework import serializers
from .models import Order, UsedMaterial, ProductionStep, ProductionStepExecution, ProductionOutput


class UsedMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    available_quantity = serializers.SerializerMethodField()
    workcenter_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UsedMaterial
        fields = [
            "id",
            "order",
            "material",
            "material_name",
            "quantity",
            "step_execution",
            "available_quantity",
            "workcenter_name",
        ]
    
    def get_available_quantity(self, obj):
        """Get available quantity of material in the workcenter location"""
        if obj.pk:  # For existing records
            wc_loc = obj._get_workcenter_location()
            if wc_loc:
                try:
                    stock_level = obj.material.stocklevel_set.get(location=wc_loc)
                    return stock_level.quantity
                except:
                    return 0
        return None
    
    def get_workcenter_name(self, obj):
        """Get workcenter name where material will be deducted from"""
        wc_loc = obj._get_workcenter_location()
        if wc_loc and wc_loc.work_center:
            return wc_loc.work_center.name
        return None


class ProductionStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionStep
        fields = [
            "id",
            "name",
            "step_type",
            "description",
            "duration_hours",
            "is_required",
            "order_sequence",
        ]


class ProductionStepExecutionSerializer(serializers.ModelSerializer):
    production_step_name = serializers.CharField(source='production_step.name', read_only=True)
    assigned_operator_name = serializers.CharField(source='assigned_operator.get_full_name', read_only=True)
    
    class Meta:
        model = ProductionStepExecution
        fields = [
            "id",
            "order",
            "production_step",
            "production_step_name",
            "status",
            "assigned_operator",
            "assigned_operator_name",
            "work_center",
            "start_time",
            "end_time",
            "actual_duration_hours",
            "notes",
            "quality_notes",
            "quantity_processed",
        ]


class ProductionOutputSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductionOutput
        fields = [
            "id",
            "step_execution",
            "product",
            "product_name",
            "unit_of_measure",
            "quantity",
            "weight",
            "quality_status",
            "notes",
        ]


class OrderSerializer(serializers.ModelSerializer):
    used_materials = UsedMaterialSerializer(many=True, read_only=True)
    step_executions = ProductionStepExecutionSerializer(many=True, read_only=True)
    produced_product_name = serializers.CharField(source='produced_product.name', read_only=True)
    operators_names = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    current_step = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "produced_product",
            "produced_product_name",
            "unit_of_measure",
            "produced_quantity",
            "operators",
            "operators_names",
            "status",
            "description",
            "start_date",
            "completion_date",
            "created_at",
            "used_materials",
            "step_executions",
            "completion_percentage",
            "current_step",
        ]
    
    def get_operators_names(self, obj):
        return [operator.get_full_name() for operator in obj.operators.all()]
    
    def get_completion_percentage(self, obj):
        return obj.get_completion_percentage()
    
    def get_current_step(self, obj):
        current = obj.get_current_step()
        if current:
            return ProductionStepExecutionSerializer(current).data
        return None


