"""
URL configuration for ayina_couture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# Set admin site header
admin.site.site_header = "Ayina Couture Administration"

# Custom 404 error handler
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Set the global 404 handler
handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('quickcheckout/', include('quickcheckout.urls')),
    path('profile/', include('profiles.urls')),
    path('wishlist/', include('wishlist.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
