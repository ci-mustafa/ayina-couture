from django.shortcuts import render
from . import models


# Products view
def all_products(request):
    products = models.Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/products.html', context)
