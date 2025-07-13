from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from offers.models import Offer
from products.models import Product

class OfferAPITestCase(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(
            name="Product A",
            description="Description A",
            slug="product-a",
            wholesale_price=100,
            market_price_increase_type="fixed",
            market_price_increase_rate=20
        )
        self.product2 = Product.objects.create(
            name="Product B",
            description="Description B",
            slug="product-b",
            wholesale_price=150,
            market_price_increase_type="percent",
            market_price_increase_rate=10
        )

        self.offer_data = {
            "name": "Summer Deal",
            "description": "10% off summer bundle",
            "slug": "summer-deal",
            "is_item_active": True,
            "products": [self.product1.id, self.product2.id],
            "discount_rate_type": "percent",
            "discount_rate_value": 10.0
        }

    def test_create_offer(self):
        url = reverse("offers-list")
        response = self.client.post(url, self.offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(Offer.objects.first().name, "Summer Deal")

    def test_list_offers(self):
        Offer.objects.create(
            name="Spring Sale",
            description="Discounted bundle",
            slug="spring-sale",
            is_item_active=True,
            discount_rate_type="fixed",
            discount_rate_value=50.0
        )
        url = reverse("offers-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_offer_detail(self):
        offer = Offer.objects.create(
            name="Spring Sale",
            description="Discounted bundle",
            slug="spring-sale",
            is_item_active=True,
            discount_rate_type="fixed",
            discount_rate_value=50.0
        )
        url = reverse("offers-detail", kwargs={"pk": offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Spring Sale")

    def test_update_offer(self):
        offer = Offer.objects.create(
            name="Old Deal",
            description="Old desc",
            slug="old-deal",
            is_item_active=False,
            discount_rate_type="fixed",
            discount_rate_value=30.0
        )
        url = reverse("offers-detail", kwargs={"pk": offer.id})
        updated_data = {
            "name": "Updated Deal",
            "description": "New desc",
            "slug": "updated-deal",
            "is_item_active": True,
            "products": [],
            "discount_rate_type": "fixed",
            "discount_rate_value": 25.0
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Deal")

    def test_delete_offer(self):
        offer = Offer.objects.create(
            name="To Be Deleted",
            description="Temporary",
            slug="to-be-deleted",
            is_item_active=True,
            discount_rate_type="fixed",
            discount_rate_value=5.0
        )
        url = reverse("offers-detail", kwargs={"pk": offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=offer.id).exists())
