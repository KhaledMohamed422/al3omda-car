from rest_framework import serializers

class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False)
    offer_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if not data.get("product_id") and not data.get("offer_id"):
            raise serializers.ValidationError("Must include either product_id or offer_id.")
        if data.get("product_id") and data.get("offer_id"):
            raise serializers.ValidationError("Cannot include both product_id and offer_id.")
        return data

class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False)
    offer_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(min_value=1)
