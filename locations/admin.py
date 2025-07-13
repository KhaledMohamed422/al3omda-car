from django.contrib import admin
from .models import Governorate, City

# Register your models here.


class GovernorateAdmin(admin.ModelAdmin):
    list_display = ('governorate_name_ar',)
    search_fields = ('governorate_name_ar', 'governorate_name_en')  

class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name_ar',)
    search_fields = ('city_name_ar', 'city_name_en')
    list_filter = ('city_name_ar', 'governorate')  # Filter by governorate

admin.site.register(Governorate, GovernorateAdmin)
admin.site.register(City, CityAdmin)


