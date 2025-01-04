from django.shortcuts import render
from . import models


# Products view
def all_products(request):
    products = models.Product.objects.all()
    ratings_range = range(1, 6)  # range from 1 to 5 for the stars
    context = {
        'products': products,
        'rating_range': ratings_range
    }
    return render(request, 'products/products.html', context)
