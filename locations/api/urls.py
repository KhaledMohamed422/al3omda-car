from rest_framework.routers import DefaultRouter
from .views import GovernorateViewSet, CityViewSet

router = DefaultRouter()
router.register('governorates', GovernorateViewSet, basename='governorates')
router.register('cities', CityViewSet, basename='cities')

urlpatterns = router.urls
