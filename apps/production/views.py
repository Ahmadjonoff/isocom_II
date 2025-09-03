from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, UsedMaterial, ProductionStep, ProductionStepExecution, ProductionOutput
from .serializers import (
    OrderSerializer, UsedMaterialSerializer, ProductionStepSerializer,
    ProductionStepExecutionSerializer, ProductionOutputSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects.select_related(
            "produced_product"
        ).prefetch_related(
            "operators", "used_materials", "step_executions__production_step"
        ).all().order_by("-created_at")
    )
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "produced_product", "unit_of_measure", "operators"]
    search_fields = ["description", "produced_product__name"]
    ordering_fields = ["id", "created_at", "produced_quantity", "start_date", "completion_date"]


class UsedMaterialViewSet(viewsets.ModelViewSet):
    queryset = UsedMaterial.objects.select_related("order", "material", "step_execution").all().order_by("id")
    serializer_class = UsedMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["order", "material", "step_execution"]
    search_fields = ["material__name"]
    ordering_fields = ["id", "quantity"]


class ProductionStepViewSet(viewsets.ModelViewSet):
    queryset = ProductionStep.objects.all().order_by("order_sequence")
    serializer_class = ProductionStepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["step_type", "is_required"]
    search_fields = ["name", "description"]
    ordering_fields = ["id", "order_sequence", "duration_hours"]


class ProductionStepExecutionViewSet(viewsets.ModelViewSet):
    queryset = ProductionStepExecution.objects.select_related(
        "order", "production_step", "assigned_operator", "work_center"
    ).all().order_by("-created_at")
    serializer_class = ProductionStepExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["order", "production_step", "status", "assigned_operator", "work_center"]
    search_fields = ["notes", "quality_notes"]
    ordering_fields = ["id", "start_time", "end_time", "actual_duration_hours"]


class ProductionOutputViewSet(viewsets.ModelViewSet):
    queryset = ProductionOutput.objects.select_related("step_execution", "product").all().order_by("-created_at")
    serializer_class = ProductionOutputSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["step_execution", "product", "quality_status"]
    search_fields = ["product__name", "notes"]
    ordering_fields = ["id", "quantity"]


