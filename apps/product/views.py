from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductComponent
from .serializers import ProductSerializer, ProductComponentSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "is_active", "price"]
    search_fields = ["name", "code", "slug", "description", "price"]
    ordering_fields = ["id", "name", "code", "updated_at", "price"]

class ProductComponentViewSet(viewsets.ModelViewSet):
    queryset = ProductComponent.objects.all().order_by("id")
    serializer_class = ProductComponentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["finished_product", "semi_finished_product"]
    search_fields = ["finished_product__name", "semi_finished_product__name"]
    ordering_fields = ["id", "finished_product", "semi_finished_product", "updated_at"]
