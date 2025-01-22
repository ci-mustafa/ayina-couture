from django.contrib import admin
from .models import Wishlist


# Wishlist admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user_username', 'product_name', 'created_at']

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = "User"

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = "Product"

