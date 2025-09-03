from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import WorkCenter
from .serializers import WorkCenterSerializer


class WorkCenterViewSet(viewsets.ModelViewSet):
    queryset = WorkCenter.objects.all().order_by("id")
    serializer_class = WorkCenterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "is_active"]
    search_fields = ["name", "description", "location"]
    ordering_fields = ["id", "name", "last_maintenance_date"]


