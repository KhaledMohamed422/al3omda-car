from rest_framework import serializers
from products.models import Product
from offers.models import Offer


class CartAddSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField(required=False)
    offer_uuid = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if not data.get("product_uuid") and not data.get("offer_uuid"):
            raise serializers.ValidationError("Either product_uuid or offer_uuid must be provided.")

        if data.get("product_uuid"):
            if not Product.objects.filter(uuid=data["product_uuid"]).exists():
                raise serializers.ValidationError({"product_uuid": "Product not found."})

        if data.get("offer_uuid"):
            if not Offer.objects.filter(uuid=data["offer_uuid"]).exists():
                raise serializers.ValidationError({"offer_uuid": "Offer not found."})

        return data


class CartUpdateSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField(required=False)
    offer_uuid = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if not data.get("product_uuid") and not data.get("offer_uuid"):
            raise serializers.ValidationError("Either product_uuid or offer_uuid must be provided.")

        if data.get("product_uuid"):
            if not Product.objects.filter(uuid=data["product_uuid"]).exists():
                raise serializers.ValidationError({"product_uuid": "Product not found."})

        if data.get("offer_uuid"):
            if not Offer.objects.filter(uuid=data["offer_uuid"]).exists():
                raise serializers.ValidationError({"offer_uuid": "Offer not found."})

        return data
