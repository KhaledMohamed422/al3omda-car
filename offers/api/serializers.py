from rest_framework import serializers
from offers.models import Offer, OfferImage
from products.api.serializers import ProductSerializer

class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImage
        fields = ['image', 'order']

class OfferSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offer-detail',  # ✅ must match router-generated name
        lookup_field='uuid',  # Use UUID for URL lookup
    )
    products = ProductSerializer(many=True, read_only=True)
    images = OfferImageSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    price_before_discount = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = [
            'url',
            'name',
            'description',
            'products',
            'price_before_discount',
            'final_price',
            'images'
        ]
