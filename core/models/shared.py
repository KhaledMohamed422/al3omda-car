from django.db import models
from core.models.base import TimeStampedModel

class Category(TimeStampedModel):
    """
    Represents a type of product accessories.
    """
    name = models.CharField(max_length=50,unique=True,help_text="دخل اسم الفئة",verbose_name="اسم الفئة")    
    slug = models.SlugField(unique=True,max_length=50)

    def __str__(self):
        return self.name

class TruckType(TimeStampedModel):
    """
    Represents a type of truck.
    """
    name = models.CharField(max_length=50,unique=True,help_text="دخل اسم الشاحنة",verbose_name="اسم الشاحنة")    
    slug = models.SlugField(unique=True,max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    country_name_ar = models.CharField(max_length=50, unique=True, help_text="دخل اسم الدولة باللغة العربية",verbose_name="اسم الدولة")
    country_name_en = models.CharField(max_length=50, unique=True, help_text="دخل اسم الدولة باللغة الإنجليزية")
    slug = models.SlugField(unique=True, max_length=50)
    
    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['country_name_ar']

    def __str__(self):
        return self.country_name_ar


