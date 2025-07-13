# admin.py
from django.contrib import admin
from .models import Order, OrderItem
from django.core.exceptions import ValidationError
from orders.forms import OrderItemForm  # ✅ Import custom form

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    min_num = 1
    form = OrderItemForm  # ✅ Use custom form

    autocomplete_fields = ['product','offer']
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': (
                'customer_name',
                'email',
                'government',
                'city',
                'address',
                'status',
                'type_deliver',
                'notes',
            )
        }),
        ('Order Price', {
            'fields': (
                'order_number',
                'get_total_price'
            ),
        }),
    )
    readonly_fields = ('order_number', 'get_total_price')
    list_display = (
        'order_number',
        'customer_name',
        'email',
        'get_total_price',
        'government',
        'city',
        'address',
        'status',
        'type_deliver',
        'created_at',
        'updated_at',
        'notes',
    )
    list_filter = ('status', 'type_deliver', 'created_at')
    search_fields = ('customer_name', 'email', 'order_number')
    # list_editable = ['status', 'type_deliver', 'notes']