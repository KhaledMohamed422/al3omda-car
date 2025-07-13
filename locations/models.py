from django.db import models


class Governorate(models.Model):
    governorate_name_ar = models.CharField(max_length=50, unique=True, null=True, blank=True,help_text="دخل اسم المحافظة باللغة العربية",verbose_name="اسم المحافظة")
    governorate_name_en = models.CharField(max_length=50, unique=True, null=True, blank=True,help_text="دخل اسم المحافظة باللغة الإنجليزية")
    
    class Meta:
        verbose_name_plural = 'Governorates'
        ordering = ['governorate_name_ar']

    def __str__(self):
        return self.governorate_name_ar

class City(models.Model):
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name='cities')
    city_name_ar = models.CharField(max_length=50, unique=True,null=True ,blank=True,help_text="دخل اسم المدينة باللغة العربية",verbose_name="اسم المدينة")
    city_name_en = models.CharField(max_length=50, unique=True,null=True ,blank=True, help_text="دخل اسم المدينة باللغة الإنجليزية")

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name_ar


