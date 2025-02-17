from django.urls import path
from . import views

urlpatterns = [
    # View cart
    path('', views.view_cart, name='view-cart'),
    # Add item
    path('add/<id>/', views.add_to_cart, name='add-to-cart'),
    # Delete item without size
    path('delete/<id>/', views.delete_cart_item, name='delete-cart-item'),
    # Delete item with size
    path('delete/<id>/<size>/', views.delete_cart_item,
         name='delete-cart-item'),
    # Delete item with size and color
    path('delete/<id>/<size>/<color>/', views.delete_cart_item,
         name='delete-cart-item'),
    # Update item with size
    path('update/<id>/<size>/', views.update_cart_item,
         name='update-cart-item'),
    # Update item without size
    path('update/<id>/', views.update_cart_item,
         name='update-cart-item'),
    path('update/<id>/<size>/<color>/', views.update_cart_item,
         name='update-cart-item'),
    path('delete-all-cart-items/', views.delete_all_cart_items,
         name='delete-all-cart-items'),
]
