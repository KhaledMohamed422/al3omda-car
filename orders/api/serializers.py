from rest_framework import serializers
from orders.models import Order, OrderItem
from products.models import Product
from offers.models import Offer

class OrderItemCreateSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField(required=False)
    offer_uuid = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if not data.get("product_uuid") and not data.get("offer_uuid"):
            raise serializers.ValidationError("Either product_uuid or offer_uuid is required.")

        if data.get("product_uuid"):
            if not Product.objects.filter(uuid=data["product_uuid"]).exists():
                raise serializers.ValidationError({"product_uuid": "Invalid product UUID"})

        if data.get("offer_uuid"):
            if not Offer.objects.filter(uuid=data["offer_uuid"]).exists():
                raise serializers.ValidationError({"offer_uuid": "Invalid offer UUID"})

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)
    total_price = serializers.DecimalField(
        source='get_total_price', 
        max_digits=10, decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'email',
            'government', 'city', 'address', 'status', 'type_deliver', 'notes',
            'items', 'total_price'
        ]
        read_only_fields = ['id', 'order_number', 'status', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item in items_data:
            if item.get("product_uuid"):
                product = Product.objects.get(uuid=item["product_uuid"])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"]
                )
            elif item.get("offer_uuid"):
                offer = Offer.objects.get(uuid=item["offer_uuid"])
                OrderItem.objects.create(
                    order=order,
                    offer=offer,
                    quantity=item["quantity"]
                )

        return order
