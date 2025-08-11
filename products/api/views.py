from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q

from products.models import Product, ProductDiscount
from products.api.serializers import (
    ProductSerializer,
    ProductDiscountSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_item_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'  # Use UUID in URLs

    @action(detail=False, methods=['get'])
    def new(self, request):
        new_products = Product.objects.filter(is_item_new=True, is_item_active=True)
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        last_products = Product.objects.filter(is_item_active=True).order_by('-id')[:20]
        serializer = self.get_serializer(last_products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_uuid', openapi.IN_QUERY,
                description="Category UUID to filter by",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            ),
            openapi.Parameter(
                'truck_uuid', openapi.IN_QUERY,
                description="Truck Type UUID to filter by",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            ),
            openapi.Parameter(
                'country_uuid', openapi.IN_QUERY,
                description="Country UUID to filter by",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def filter_products(self, request):
        """General filtering by category, truck type, country, or any combination (based on UUIDs)."""
        category_uuid = request.query_params.get('category_uuid')
        truck_uuid = request.query_params.get('truck_uuid')
        country_uuid = request.query_params.get('country_uuid')

        filters = Q(is_item_active=True)

        if category_uuid:
            filters &= Q(categories__uuid=category_uuid)
        if truck_uuid:
            filters &= Q(truck__uuid=truck_uuid)
        if country_uuid:
            filters &= Q(countries__uuid=country_uuid)

        products = Product.objects.filter(filters).distinct()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='uuid',
                in_=openapi.IN_QUERY,
                description='UUID of the product to find similar products for',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True
            )
        ],
        responses={
            200: ProductSerializer(many=True),
            400: openapi.Response(
                description='Bad Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            ),
            404: openapi.Response(
                description='Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            )
        }
    )
    @action(detail=False, methods=['get'])
    def similar_products(self, request):
        """Get similar products based on the current product's categories."""
        product_uuid = request.query_params.get('uuid')
        if not product_uuid:
            return Response({"detail": "Product UUID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(uuid=product_uuid, is_item_active=True)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        similar_products = Product.objects.filter(
            categories__in=product.categories.all(),
            is_item_active=True
        ).exclude(id=product.id).distinct()

        # If no similar products, get 5 random ones
        if similar_products.count() == 0:
            similar_products = Product.objects.filter(
                is_item_active=True
            ).exclude(id=product.id).order_by('?')[:5]

        # If fewer than 5, fill up with random active products
        elif similar_products.count() < 5:
            existing_ids = list(similar_products.values_list('id', flat=True)) + [product.id]
            needed = 5 - similar_products.count()
            more = Product.objects.filter(
                is_item_active=True
            ).exclude(id__in=existing_ids).order_by('?')[:needed]
            similar_products = list(similar_products) + list(more)

        serializer = self.get_serializer(similar_products, many=True)
        return Response(serializer.data)
