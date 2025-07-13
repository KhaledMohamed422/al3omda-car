from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from products.models import Product, ProductDiscount, ProductImage
from products.api.serializers import (
    ProductSerializer,
    ProductDiscountSerializer,
    ProductImageSerializer,
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_item_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def new(self, request):
        new_products = Product.objects.filter(is_item_new=True, is_item_active=True)
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)


class ProductDiscountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductDiscount.objects.filter(active=True)
    serializer_class = ProductDiscountSerializer
    permission_classes = [AllowAny]


class ProductImageListView(generics.ListAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return ProductImage.objects.filter(product_id=product_id)