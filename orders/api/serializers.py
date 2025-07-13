from rest_framework import serializers
from orders.models import Order, OrderItem
from products.models import Product
from offers.models import Offer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    offer_name = serializers.CharField(source="offer.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'offer', 'offer_name', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'email',
            'government', 'city', 'address', 'status', 'type_deliver', 'notes',
            'items', 'total_price'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order
