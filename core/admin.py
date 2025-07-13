# core/admin/project_info.py
# cspell:words tiktok

from django.contrib import admin
from core.models.shared import Category, Country, TruckType
from core.models.project_info import ProjectInfo


# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ('name',)
    list_display = ['name',]


# Admin for Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['country_name_ar', 'country_name_en']
    fields = ('country_name_ar', 'country_name_en')
    list_display = ['country_name_ar',]

# Admin for TruckType
@admin.register(TruckType)
class TruckTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ('name',)
    list_display = ['name',]


# Admin for ProjectInfo
@admin.register(ProjectInfo)
class ProjectInfoAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not ProjectInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = ((
        "Contact Information", {
            'fields': ('site_name','contact_email', 'support_phone', 'whatsapp_number')
        }),
        ('Social Media', {
            'fields': ('tiktok_url', 'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('Logo and Favicon', {
            'fields': ('logo', 'favicon')
        }),
        ('Project Details', {
            'fields': ('description', 'places', 'vision', 'mission', 'address')
        }),
    )