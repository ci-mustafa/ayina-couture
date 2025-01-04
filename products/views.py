from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from . import models


# Products view
def all_products(request):
    products = models.Product.objects.all()
    paginator = Paginator(products, 3)  # Show products per page
    page_number = request.GET.get('page')  # Get the current page number from the query params
    page_obj = paginator.get_page(page_number)  # Get the products for the current page
    ratings_range = range(1, 6)  # range from 1 to 5 for the stars
    top_rate_value = 5.0
    context = {
        'products': products,
        'rating_range': ratings_range,
        'top_rate_value': top_rate_value,
        'page_obj': page_obj,
        'page_number': page_number
    }
    return render(request, 'products/products.html', context)


# Product detail view
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    ratings_range = range(1, 6)
    top_rate_value = 5.0
    context = {
        'product': product,
        'rating_range': ratings_range,
    }
    return render(request, 'products/product_detail.html', context)
