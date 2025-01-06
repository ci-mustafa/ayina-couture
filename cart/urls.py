from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view-cart'),
    path('add/<id>/', views.add_to_cart, name='add-to-cart'),
    path('update/<id>/', views.update_cart_item, name='update-cart-item'),
    path('update/<id>/<size>', views.update_cart_item, name='update-cart-item'),
    # Delete item without size
    path('delete/<id>/', views.delete_cart_item, name='delete-cart-item'),
    # Delete item with size 
    path('delete/<id>/<size>/', views.delete_cart_item, name='delete-cart-item'),  

]