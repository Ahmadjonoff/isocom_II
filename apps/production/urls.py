from rest_framework.routers import DefaultRouter
from .views import (
    UsedMaterialViewSet, OrderViewSet, ProductionStepViewSet,
    ProductionStepExecutionViewSet, ProductionOutputViewSet
)


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'used-materials', UsedMaterialViewSet, basename='usedmaterial')
router.register(r'production-steps', ProductionStepViewSet, basename='productionstep')
router.register(r'step-executions', ProductionStepExecutionViewSet, basename='productionstepexecution')
router.register(r'production-outputs', ProductionOutputViewSet, basename='productionoutput')


urlpatterns = router.urls


