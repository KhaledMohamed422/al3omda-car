from rest_framework import serializers
from products.models import Product, ProductDiscount, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']


class ProductDiscountSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductDiscount
        fields = ['id', 'product', 'discount_type', 'value', 'start_at', 'end_at', 'active']


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',  # name from your urls/router
        lookup_field='uuid'          # tell DRF to use uuid instead of pk
    )

    categories = serializers.StringRelatedField(many=True)
    countries = serializers.StringRelatedField(many=True)
    truck = serializers.StringRelatedField(many=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    images = ProductImageSerializer(source="images.all", many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'url','name', 'description', 'uuid','market_price', 'final_price', 'categories', 'countries', 'truck', 'images'
        ]