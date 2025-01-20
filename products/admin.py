from django.contrib import admin
from . import models


# CollectionAdmin
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'display_name',
    ]

# ColorAdmin
@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'products__name']
    fields = ['name', 'color_code']

# ProductAdmin 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'sku','name', 'image','description', 'display_colors', 'material', 'price',
        'has_sizes', 'stock_quantity',
        'collection__title'
    ]
    filter_horizontal = ['color']  # Allows easy selection of multiple colors

    # Custom method to display colors
    def display_colors(self, obj):
        """
        Returns a comma-separated list of colors for the product.
        """
        return ", ".join([color.name for color in obj.color.all()])

    display_colors.short_description = "Colors"

# ProductRatingAdmin
@admin.register(models.ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = [
        'product__name',
        'user__username',
        'rating',
        'created_at'
    ]
