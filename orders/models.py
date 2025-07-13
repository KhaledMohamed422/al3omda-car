from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from offers.models import Offer
from django.core.validators import MinValueValidator
from locations.models import Governorate,City   
import secrets
from django.db.models import Q
from core.models.base import TimeStampedModel 


def generate_order_number():
    # generates a 20-char hex string
    return secrets.token_hex(7)

class Order(TimeStampedModel):

    STATUS_CHOICES = [
        ('pending', _('فانتظار تأكيد الطلب من العميل')),
        ('processing', _('يتم تجهيز الطلبية')),
        ('delivered', _('تم التوصيل')),
        ('cansaled',  _('تم الغاء الطلب'))
    ]

    DELIVERY_TYPE_CHOICES = [
        ('home', _('توصيل عادي')),
        ('pickup', _('توصيل سريع')),
        ('self', _('استلام من المتجر')),
    ]


    customer_name = models.CharField(max_length=100,verbose_name="اسم العميل",help_text="دخل اسم العميل")
    email = models.EmailField(verbose_name="ايميل العميل",help_text="دخل ايميل العميل")
    government = models.ForeignKey(Governorate, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="المحافظة اللي ساكن فيها العميل")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="المدينة اللي ساكن فيها العميل")
    address = models.TextField(verbose_name="عنوان العميل بالتفصيل")

    order_number = models.CharField(max_length=20,unique=True,default=generate_order_number,editable=False,verbose_name="رقم الطلب")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',verbose_name="تتبع تسليم الطلب")
    type_deliver = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='home',verbose_name="طريقة توصيل الطلب؟")
    notes = models.TextField(blank=True, null=True,verbose_name="ملاحظات عن الطلب",help_text="سجل اي ملاحظات متعلقة بالطلب")

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"

    @property
    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(TimeStampedModel):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.PROTECT,null=True, blank=True,related_name="order_items",verbose_name="المنتج اللي العميل طلبه")
    offer = models.ForeignKey(Offer,on_delete=models.PROTECT,null=True, blank=True,related_name="order_items",verbose_name="العرض اللي العميل  طلبه")
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)],verbose_name="الكمية")

    @property
    def total_price(self):
        if self.product:
            return self.quantity * self.product.final_price
        elif self.offer:
            return self.quantity * self.offer.final_price

    def __str__(self):
        target = self.product or self.offer
        return f"{target.name} x{self.quantity}"

