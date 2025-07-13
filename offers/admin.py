from django.contrib import admin
from offers.models import Offer, OfferImage
from django.utils.html import format_html
from core.models.shared import Category, Country, TruckType

# Inline admin for OfferImage with preview and order support
class OfferImageInline(admin.TabularInline):
    model = OfferImage
    fields = ['image_preview', 'image', 'order']
    readonly_fields = ['image_preview']
    extra = 0
    min_num = 1

    def image_preview(self, obj=None):
        if obj and obj.image:
            return format_html(
                '<img id="preview_id_images-{}-image" src="{}" style="max-height:100px;" />',
                obj.pk,
                obj.image.url
            )
        return format_html(
            '<img id="preview_id_images-__prefix__-image" style="max-height:100px; display:none;" />'
        )

    image_preview.short_description = 'Preview'



# Admin for Offer
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = [OfferImageInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'products','description')
        }),
        ('Pricing', {
            'fields': (
                'discount_rate_type', 'discount_rate_value', 'price_before_discount', 'price_after_discount'
            )
        }),
        ('Advanced Options', {
            'fields': ('is_item_active',)
        }),
    )


    autocomplete_fields = ['products',]
    readonly_fields = ['price_before_discount','price_after_discount',]
    list_display = ['name', 'price_before_discount', 'price_after_discount', 'is_item_active','created_at','updated_at']
    list_editable = ['is_item_active',]
    search_fields = ['name']

    def price_before_discount(self, obj):
        return obj.price_before_discount

    def price_after_discount(self, obj):
        return obj.price_after_discount
    
    price_before_discount.short_description = 'السعر قبل الخصم'
    price_after_discount.short_description = 'السعر بعد الخصم'