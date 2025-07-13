from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Product
from offers.models import Offer

class CartAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a product and offer
        self.product = Product.objects.create(name="Test Product", final_price=100)
        self.offer = Offer.objects.create(name="Test Offer", price=200, price_after_discount=150)

    def test_add_product_to_cart(self):
        response = self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 2
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("cart", self.client.session)
        self.assertEqual(self.client.session["cart"][0]["quantity"], 2)

    def test_add_offer_to_cart(self):
        response = self.client.post("/api/cart/add/", {
            "offer_id": self.offer.id,
            "quantity": 1
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.session["cart"][0]["offer_id"], self.offer.id)

    def test_get_cart_items(self):
        # Add item first
        self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 3
        }, format='json')

        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["quantity"], 3)

    def test_update_cart_quantity(self):
        self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 2
        }, format='json')

        response = self.client.patch("/api/cart/update/", {
            "product_id": self.product.id,
            "quantity": 5
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["cart"][0]["quantity"], 5)

    def test_remove_cart_item(self):
        self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 2
        }, format='json')

        response = self.client.delete(f"/api/cart/remove/?product_id={self.product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session.get("cart", [])), 0)

    def test_cart_total(self):
        self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 2
        }, format='json')
        self.client.post("/api/cart/add/", {
            "offer_id": self.offer.id,
            "quantity": 1
        }, format='json')

        response = self.client.get("/api/cart/total/")
        self.assertEqual(response.status_code, 200)
        expected_total = 2 * self.product.final_price + self.offer.price_after_discount
        self.assertEqual(response.data["total"], expected_total)

    def test_cart_count(self):
        self.client.post("/api/cart/add/", {
            "product_id": self.product.id,
            "quantity": 3
        }, format='json')
        self.client.post("/api/cart/add/", {
            "offer_id": self.offer.id,
            "quantity": 2
        }, format='json')

        response = self.client.get("/api/cart/count/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
