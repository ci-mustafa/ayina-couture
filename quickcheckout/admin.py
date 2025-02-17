from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('order_item_total', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline, )
    fields = (
        'order_number', 'user', 'full_name', 'email', 'phone_number', 
        'country', 'postcode', 'city', 'street_address', 'status', 
        'delivery_cost', 'order_cost', 'order_final_total',
        'created_at', 'updated_at'
    )
    readonly_fields = ('order_number', 'created_at', 'updated_at',
                      'order_cost', 'delivery_cost', 'order_final_total')
    list_display = ('order_number', 'full_name', 
                    'email', 'status', 'order_cost', 
                    'delivery_cost', 'order_final_total', 
                    'created_at',)
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'status')
    ordering = ['-created_at']





