from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import StockLevel, InventoryMovementLog
from .serializers import StockLevelSerializer, InventoryMovementLogSerializer


class StockLevelViewSet(viewsets.ModelViewSet):
    queryset = StockLevel.objects.select_related("material", "location").all().order_by("id")
    serializer_class = StockLevelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["material", "location"]
    search_fields = []
    ordering_fields = ["id", "quantity"]


class InventoryMovementLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovementLog.objects.select_related(
        "material", "from_location", "to_location"
    ).all().order_by("-created_at")
    serializer_class = InventoryMovementLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["material", "from_location", "to_location"]
    search_fields = []
    ordering_fields = ["id", "created_at", "quantity"]


