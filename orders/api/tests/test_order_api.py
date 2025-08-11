from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from orders.models import Order, OrderItem
from products.models import Product
from offers.models import Offer
from locations.models import Governorate, City


class OrderAPITestCase(APITestCase):

    def setUp(self):
        self.gov = Governorate.objects.create(name='Cairo')
        self.city = City.objects.create(name='Nasr City', governorate=self.gov)

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Desc",
            wholesale_price=100,
            market_price_increase_type="fixed",
            market_price_increase_rate=50,
            is_item_active=True,
            is_item_new=True,
        )

        self.offer = Offer.objects.create(
            name="Test Offer",
            description="Offer Desc",
            price=200,
            is_item_active=True,
        )

        self.order_payload = {
            "customer_name": "Ahmed",
            "email": "ahmed@example.com",
            "government": self.gov.id,  # locations still probably use int PK
            "city": self.city.id,
            "address": "123 Main St",
            "type_deliver": "home",
            "notes": "Please deliver fast",
            "items": [
                {"product": str(self.product.uuid), "quantity": 2},
                {"offer": str(self.offer.uuid), "quantity": 1},
            ]
        }

    def test_create_order(self):
        url = reverse("orders-list")
        response = self.client.post(url, self.order_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_list_orders(self):
        self.test_create_order()
        url = reverse("orders-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_order(self):
        self.test_create_order()
        order = Order.objects.first()
        url = reverse("orders-detail", args=[order.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customer_name"], "Ahmed")

    def test_create_order_invalid_missing_items(self):
        url = reverse("orders-list")
        invalid_payload = self.order_payload.copy()
        invalid_payload.pop("items")
        response = self.client.post(url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_total_price_property(self):
        self.test_create_order()
        order = Order.objects.first()
        expected_total = (
            self.product.final_price * 2 +
            self.offer.final_price * 1
        )
        self.assertEqual(order.get_total_price, expected_total)
