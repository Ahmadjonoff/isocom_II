from rest_framework.routers import DefaultRouter
from .views import WorkCenterViewSet


router = DefaultRouter()
router.register(r'workcenters', WorkCenterViewSet, basename='workcenter')


urlpatterns = router.urls


