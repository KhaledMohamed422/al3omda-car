from django.db import models
from core.models.base import BaseItem,BaseImage
from products.models import Product
from core.models.base import UploadToSlugFolder
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Offer(BaseItem):
    """
    Model representing an offer.
    """
    PERCENT = 'percent'
    FIXED = 'fixed'
    DISCOUNT_PRICE_TYPE_CHOICES = [
        (PERCENT, _('نسبة مئوية')),
        (FIXED, _('مبلغ ثابت')),
    ]


    products = models.ManyToManyField(Product, related_name='offers', null=True,blank=True, help_text="اختر المنتجات التي تريد تضمينها في هذا العرض")
    discount_rate_type = models.CharField(max_length=10, choices=DISCOUNT_PRICE_TYPE_CHOICES,default=FIXED,help_text=_("اختار نوع العملية الحسابية الذي ستطبق علي سعر العرض")) # Increase type (choice)
    discount_rate_value = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)],help_text=_("دخل قيمة معدل الخصم لسعر العرض"))# Increase rate (input)
    
    @property
    def price_before_discount(self):
        """
        Returns the total number of products included in the offer.
        """
        return sum(product.final_price for product in self.products.all())
    
    @property
    def price_after_discount(self):
        """
        Calculate the total price of the offer based on the products included.
        """
        if self.discount_rate_type == self.PERCENT:
            return max(self.price_before_discount * (1 - self.discount_rate_value / 100),0)
        return max(self.price_before_discount - self.discount_rate_value, 0)
    
    @property
    def final_price(self):
        """
        Returns the final price after applying the discount.
        """
        return self.price_after_discount
    
    def __str__(self):
        return self.name
    

class OfferImage(BaseImage):
    """
    Model representing an image associated with an offer.
    """
    offer = models.ForeignKey(Offer, related_name='images', on_delete=models.CASCADE, help_text="اختر العرض الذي تريد ربط هذه الصورة به")
    
    class Meta:
        verbose_name = "Offer Image"
        verbose_name_plural = "Offer Images"
        ordering = ['order', 'id']  # Ensures consistent ordering

    
    constraints = [
        models.UniqueConstraint(fields=['offer', 'order'], name='unique_image_order_per_product')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('image').upload_to = UploadToSlugFolder('offer')
