from django.db import models
from core.models.base import BaseItem , BaseDiscount , BaseImage , UploadToUuidFolder
from core.models.shared import Category, TruckType, Country
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator,FileExtensionValidator
import math
    
class Product(BaseItem):
    """
    Represents a product in the e-commerce system.
    """

    PERCENT = 'percent'
    FIXED = 'fixed'
    
    MARKET_PRICE_TYPE_CHOICES = [
        (PERCENT, _('نسبة مئوية')),
        (FIXED, _('مبلغ ثابت')),
    ]


    # سعر الجملة
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.0)],help_text=_("دخل سعر الجملة"),verbose_name="سعر الجملة") # Wholesale price (input)
    # معدل الزيادة فسعر الجملة لانتاج سعر للسوق
    market_price_increase_type = models.CharField(max_length=10, choices=MARKET_PRICE_TYPE_CHOICES,default=FIXED,help_text=_("اختار نوع العملية الحسابية الذي ستطبق علي سعر الجملة")) # Increase type (choice)
    market_price_increase_rate = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)],help_text=_("دخل قيمة معدل الزيادة لسعر الجملة"))# Increase rate (input)
    # سعر السوق
    market_price = models.PositiveIntegerField(editable=False,verbose_name="سعر المنتج فالسوق") # Final market price (read-only)
    is_item_new = models.BooleanField(default=True, help_text="هل هذا المنتج جديد؟ يعني تريد ات يظهر فالصفحة لليوزر فجزء وصلنا حديثا",verbose_name="هل المنتج جديد فالسوق؟")  # Is this item new?


    categories = models.ManyToManyField(Category,blank=True,related_name='products',help_text="دخل الفئات التي ينتمي إليها هذا المنتج")  # Select categories this product belongs to
    countries = models.ManyToManyField(Country,blank=True,related_name='products',help_text="دخل الدول التي اتصنع منها هذا المتتج")  # Select countries where this product is available
    truck = models.ManyToManyField(TruckType,blank=True,related_name='products',help_text="دحل الشاحنات التي يتناسب معها هذا المنتج")  # Select truck types this product is compatible with
    
    class Meta:
        ordering = ['created_at']

    @property
    def final_price(self):
        """
        Returns the market price after applying the first active discount if available.
        """
        active_discount = self.discounts.filter(active=True).first()
        if active_discount:
            return active_discount.calculate_discounted_price(self.market_price)
        return math.ceil(self.market_price)

    # Helper method to validate market price increase rate
    def calculate_market_price(self):
        if self.market_price_increase_type == self.PERCENT:
            return int(self.wholesale_price * (1 + self.market_price_increase_rate / 100))
        return math.ceil(self.wholesale_price + self.market_price_increase_rate)

    def save(self, *args, **kwargs):
        self.market_price = self.calculate_market_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductDiscount(BaseDiscount):
    """
    Represents a discount that can be applied to products.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')


    def __str__(self):
        return f"{self.product.name} - {self.value} ({self.discount_type})"

class ProductImage(BaseImage):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order', 'id']  # Ensures consistent ordering
        
    constraints = [
        models.UniqueConstraint(fields=['product', 'order'], name='unique_image_order_per_product')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('image').upload_to = UploadToUuidFolder('product')
