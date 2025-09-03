from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductComponentViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-components', ProductComponentViewSet, basename='productcomponent')


urlpatterns = router.urls