from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Warehouse, Location
from .serializers import WarehouseSerializer, LocationSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all().order_by("id")
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["id", "name", "updated_at"]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related("warehouse", "work_center").all().order_by("id")
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["location_type", "warehouse", "work_center", "is_active"]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "updated_at"]


