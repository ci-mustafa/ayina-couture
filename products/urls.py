from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('add/', views.product_add, name='product-add'),
    path('delete/<int:pk>/', views.delete_product, name='product-delete'),
]