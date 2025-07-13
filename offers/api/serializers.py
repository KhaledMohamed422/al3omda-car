from rest_framework import serializers
from offers.models import Offer, OfferImage

class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImage
        fields = ['id', 'image', 'order']

class OfferSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Offer.products.rel.model.objects.all()
    )
    images = OfferImageSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    price_before_discount = serializers.ReadOnlyField()
    price_after_discount = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = [
            'id', 'name', 'description', 'slug', 'is_item_active',
            'products', 'discount_rate_type', 'discount_rate_value',
            'price_before_discount', 'price_after_discount', 'final_price',
            'images'
        ]
