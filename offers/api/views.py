from rest_framework import viewsets
from offers.models import Offer
from offers.api.serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.prefetch_related('products', 'images').all()
    serializer_class = OfferSerializer
