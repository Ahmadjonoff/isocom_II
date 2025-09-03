from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.workcenter.models import WorkCenter
from apps.material.models import Material
from apps.product.models import Product, ProductComponent
from apps.warehouse.models import Warehouse, Location
from apps.stock.models import StockLevel, InventoryMovementLog
from apps.production.models import Order, UsedMaterial, ProductionStep, ProductionStepExecution, ProductionOutput


User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Extend the default UserAdmin with extra fields
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Extra",
            {
                "fields": (
                    "phone_number",
                    "role",
                    "employee_id",
                    "shift",
                    "profile_picture",
                )
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "shift",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "role", "shift")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    orqdering = ("-created_at", "username")


@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "location", "capacity_per_hour", "last_maintenance_date", "is_active")
    list_filter = ("type", "is_active")
    search_fields = ("name", "description", "location")
    ordering = ("-created_at", "name")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "type", "unit_of_measure", "is_active", "created_at")
    list_filter = ("type", "unit_of_measure", "is_active")
    search_fields = ("name", "code", "slug", "description")
    ordering = ("-created_at", "name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "type", "is_active", "created_at")
    list_filter = ("type", "is_active")
    search_fields = ("name", "code", "slug", "description")
    ordering = ("-created_at", "name")

@admin.register(ProductComponent)
class ProductComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "finished_product", "semi_finished_product")
    list_filter = ("finished_product", "semi_finished_product")
    search_fields = ("finished_product__name", "semi_finished_product__name")
    ordering = ("-created_at", "finished_product__name")

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("-created_at", "name")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location_type", "warehouse", "work_center", "is_active")
    list_filter = ("location_type", "is_active")
    search_fields = ("name",)
    ordering = ("-created_at", "name")


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "material", "product", "location", "quantity")
    list_filter = ("location", "material", "product")
    search_fields = ("material__name","product__name")
    ordering = ("-created_at", "material__name",)

@admin.register(InventoryMovementLog)
class InventoryMovementLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_location', 'to_location', 'material', "product", 'quantity')
    list_filter = ('from_location', 'to_location', 'material', "product")
    search_fields = ('from_location', 'to_location', 'material', "product")
    ordering = ("-created_at", )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "produced_product", "produced_quantity", "unit_of_measure", "status", "created_at")
    list_filter = ("status", "unit_of_measure", "produced_product")
    search_fields = ("description", "produced_product__name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    filter_horizontal = ("operators",)


@admin.register(UsedMaterial)
class UsedMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "material", "quantity", "step_execution")
    list_filter = ("material", "step_execution__production_step")
    search_fields = ("material__name",)
    ordering = ("-created_at",)


@admin.register(ProductionStep)
class ProductionStepAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "step_type", "order_sequence", "duration_hours", "is_required")
    list_filter = ("step_type", "is_required")
    search_fields = ("name", "description")
    ordering = ("order_sequence",)


@admin.register(ProductionStepExecution)
class ProductionStepExecutionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "production_step", "status", "assigned_operator", "start_time", "end_time")
    list_filter = ("status", "production_step__step_type", "assigned_operator")
    search_fields = ("order__produced_product__name", "notes", "quality_notes")
    ordering = ("-created_at",)
    date_hierarchy = "start_time"


@admin.register(ProductionOutput)
class ProductionOutputAdmin(admin.ModelAdmin):
    list_display = ("id", "step_execution", "product", "unit_of_measure", "quantity", "weight", "quality_status")
    list_filter = ("quality_status", "product", "unit_of_measure")
    search_fields = ("product__name", "notes")
    ordering = ("-created_at",)
