from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_wishlist, name='list-wishlist'),
    path('add/<product_id>/', views.add_to_wishlist,
         name='add-to-wishlist'),
    path('remove/<product_id>/', views.remove_wishlist_item,
         name='remove-wishlist-item'),
]