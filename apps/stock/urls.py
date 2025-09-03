from rest_framework.routers import DefaultRouter
from .views import StockLevelViewSet, InventoryMovementLogViewSet


router = DefaultRouter()
router.register(r'stock-levels', StockLevelViewSet, basename='stocklevel')
router.register(r'inventory-movement-logs', InventoryMovementLogViewSet, basename='inventorymovementlog')


urlpatterns = router.urls


