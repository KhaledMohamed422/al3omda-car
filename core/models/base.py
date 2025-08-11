from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator,FileExtensionValidator
from django.utils.deconstruct import deconstructible
import uuid

# Abstract base model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseDiscount(models.Model):
    PERCENT = 'percent'
    FIXED = 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, _('نسبة مئوية')),
        (FIXED, _('مبلغ ثابت')),
    ]

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES,default=FIXED, help_text="Select the type of discount")
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)], help_text="Enter the discount value")
    start_at = models.DateTimeField(null=True, blank=True, help_text="Leave blank for no start date")
    end_at = models.DateTimeField(null=True, blank=True, help_text="Leave blank for no end date")
    active = models.BooleanField(default=True, help_text="Is this discount currently active?")

    class Meta:
        abstract = True

    def calculate_discounted_price(self, base_price):
        if base_price is None or self.value is None:
            return None  # avoid TypeError
        if not self.active:
            return base_price
        if self.discount_type == self.PERCENT:
            return base_price * (1 - self.value / 100)
        return max(base_price - self.value, 0)

    
class BaseItem(TimeStampedModel):

    name = models.CharField(max_length=70,unique=True,help_text="دحل اسم المنتج/العرض",verbose_name="اسم المنتج/العرض")  # Name of the item
    description = models.TextField(help_text="دخل وصف المنتج/العرض",verbose_name="وصف المنتج/العرض")  # Description of the item
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # add new field called tags 
    is_item_active = models.BooleanField(default=True, help_text="هل هذا المنتج/عرض نشط؟ يعني تريد ات يظهر فالصفحة لليوزر",verbose_name="يظهر لليور؟")  # Is this item active?

    class Meta:
        abstract = True




@deconstructible
class UploadToUuidFolder:
    def __init__(self, folder_attr):
        self.folder_attr = folder_attr  # e.g. 'product' or 'offer'

    def __call__(self, instance, filename):
        related_obj = getattr(instance, self.folder_attr)
        uuid_str = str(getattr(related_obj, 'uuid', 'unknown'))
        return f"{self.folder_attr}_images/{uuid_str}/{filename}"

class BaseImage(TimeStampedModel):
    image = models.ImageField(upload_to='',validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],help_text="اختر صورة للمنتج")
    order = models.PositiveIntegerField(default=0, help_text="رتب هذه الصورة لعرضها في الترتيب الصحيح")

    class Meta:
        abstract = True


