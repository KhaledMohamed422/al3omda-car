from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from products.models import Product, ProductDiscount, ProductImage
from core.models.shared import Category, TruckType, Country
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
from django.utils import timezone


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create shared relations
        self.category = Category.objects.create(name="Engine Parts")
        self.country = Country.objects.create(country_name_ar="مصر", country_name_en="Egypt")
        self.truck = TruckType.objects.create(name="Volvo")

        # Create a product
        self.product = Product.objects.create(
            name="Brake Pads",
            description="High quality brake pads",
            wholesale_price=100,
            market_price_increase_type="fixed",
            market_price_increase_rate=50,
            is_item_active=True,
            is_item_new=True
        )
        self.product.categories.add(self.category)
        self.product.countries.add(self.country)
        self.product.truck.add(self.truck)

        # Discount
        self.discount = ProductDiscount.objects.create(
            product=self.product,
            discount_type="percent",
            value=10,
            start_at=timezone.now() - timedelta(days=1),
            end_at=timezone.now() + timedelta(days=1),
            active=True
        )

        # Product Image
        image_file = SimpleUploadedFile("test.jpg", b"image data", content_type="image/jpeg")
        self.image = ProductImage.objects.create(
            product=self.product,
            image=image_file,
            order=1
        )

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        url = reverse("product-detail", kwargs={"pk": self.product.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.product.name)

    def test_list_new_products(self):
        url = reverse("product-new")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["is_item_new"], True)

    def test_product_images(self):
        url = reverse("product-images", kwargs={"product_id": self.product.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_discounts(self):
        url = reverse("productdiscount-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_discount_detail(self):
        url = reverse("productdiscount-detail", kwargs={"pk": self.discount.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["value"], "10.00")
