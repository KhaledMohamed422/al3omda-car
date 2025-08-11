from rest_framework import viewsets, mixins
from orders.models import Order
from .serializers import OrderSerializer

class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    POST-only endpoint for creating orders.
    """
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer
