from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from . import models


# Products view
def all_products(request):
    products = models.Product.objects.all()
    query = None
    collection = None
    sort_by = request.GET.get('sort_by', None)  # Capture the sorting criteria
    if request.GET:
        # Handle Collection Filter
        if 'collection' in request.GET:
            collection = request.GET.get('collection')
            if collection:
                products = products.filter(collection__title__iexact=collection)

        # Handle Search Query
        if 'query' in request.GET:
            query = request.GET['query']
            if not query:
                messages.error(request, 'You did not enter any search data!')
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        # Handle Sorting
        if sort_by == 'price_asc':
            products = products.order_by('price')  # Sort by price ascending
        elif sort_by == 'price_desc':
            products = products.order_by('-price')  # Sort by price descending

    paginator = Paginator(products, 10)  # Show products per page
    page_number = request.GET.get('page')  # Get the current page number from the query params
    page_obj = paginator.get_page(page_number)  # Get the products for the current page
    ratings_range = range(1, 6)  # range from 1 to 5 for the stars
    top_rate_value = 5.0

    context = {
        'products': products,
        'rating_range': ratings_range,
        'top_rate_value': top_rate_value,
        'page_obj': page_obj,
        'page_number': page_number,
        'search': query,
        'collection': collection,
        'query_params': f"&query={query}" if query else '',
        'collection_params': f"&collection={collection}" if collection else '',
        'sort_by': sort_by,
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
