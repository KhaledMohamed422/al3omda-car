from rest_framework.routers import DefaultRouter
from .views import GovernorateViewSet

router = DefaultRouter()
router.register('governorates', GovernorateViewSet, basename='governorates')

urlpatterns = router.urls
