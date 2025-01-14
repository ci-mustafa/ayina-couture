from django.contrib import admin
from . import models


# CollectionAdmin
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'display_name',
    ]

# ProductAdmin 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'sku','name', 'image','description', 'material', 'price',
        'has_sizes', 'stock_quantity',
        'collection__title'
    ]

# ProductRatingAdmin
@admin.register(models.ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = [
        'product__name',
        'user__username',
        'rating',
        'created_at'
    ]
