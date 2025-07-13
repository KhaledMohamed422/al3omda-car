from django.contrib import admin
from django.utils.html import format_html
from products.models import Product, ProductImage, ProductDiscount
from core.models.shared import Category, Country, TruckType


# Inline admin for ProductImage with preview and order support
class ProductImageInline(admin.TabularInline):
    model = ProductImage
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



# Inline admin for ProductDiscount
class ProductDiscountInline(admin.TabularInline):
    model = ProductDiscount
    extra = 1
    max_num = 1
    fields = ['discount_type', 'value', 'start_at', 'end_at', 'active', 'final_price']
    readonly_fields = ['final_price']

    def final_price(self, obj):
        if not obj or not obj.product:
            return "-"
        base_price = obj.product.market_price
        if base_price is None or obj.value is None:
            return "-"
        return obj.calculate_discounted_price(base_price)

    final_price.short_description = 'Final Price'



# Admin for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductDiscountInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Pricing', {
            'fields': (
                'wholesale_price', 'market_price_increase_type',
                'market_price_increase_rate', 'market_price'
            )
        }),
        ('Categories and Availability', {
            'fields': ('categories', 'countries', 'truck')
        }),
        ('Advanced Options', {
            'fields': ('is_item_active', 'is_item_new')
        }),
    )

    autocomplete_fields = ['categories', 'truck', 'countries']
    readonly_fields = ['market_price']
    list_display = ['name', 'wholesale_price', 'market_price', 'discount_price', 'is_item_active', 'is_item_new','created_at','updated_at']
    list_editable = ['is_item_active', 'is_item_new']
    search_fields = ['name']
    list_filter = ['categories', 'countries', 'truck']

    def discount_price(self, obj):
        """
        Returns the market price after applying the first active discount.
        You can customize to pick highest or lowest or all discounts.
        """
        return obj.final_price
    
    discount_price.short_description = 'السعر النهائي بعد الخصم'