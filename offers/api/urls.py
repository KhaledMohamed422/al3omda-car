from rest_framework.routers import DefaultRouter
from .views import OfferViewSet

router = DefaultRouter()
router.register('', OfferViewSet, basename='offer')  # ✅ name = 'offer-detail'

urlpatterns = router.urls
