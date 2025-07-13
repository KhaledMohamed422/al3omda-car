from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offers.api.views import OfferViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offers')

urlpatterns = [
    path('', include(router.urls)),
]
