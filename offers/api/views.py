from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from offers.models import Offer
from .serializers import OfferSerializer

class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'  # ✅ must match serializer
