from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from . import models
from .forms import ProductForm


# Products view
def all_products(request):
    """
    Retrieve and display all products with optional filtering, searching, sorting, and pagination.

    This view supports:
    - Filtering by collection
    - Searching by product name or description
    - Sorting by price (ascending or descending)
    - Paginating results (10 products per page)

    Args:
        request (HttpRequest): The HTTP request containing optional GET parameters:
            - `collection`: Filters products by collection title (case-insensitive)
            - `query`: Searches products by name or description
            - `sort_by`: Sorts products by price (`price_asc` or `price_desc`)
            - `page`: Specifies the pagination page number

    Returns:
        HttpResponse: Renders `products.html` with the filtered and paginated product list.
    """
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

    paginator = Paginator(products, 5)  # Show products per page
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

    """
    Display the details of a specific product.

    Retrieves a product by its primary key (pk). If the product does not exist, 
    returns a 404 error. The view also provides a range for product ratings.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the product to retrieve.

    Returns:
        HttpResponse: Renders `product_detail.html` with product details.
    """
    product = get_object_or_404(models.Product, pk=pk)
    ratings_range = range(1, 6)
    top_rate_value = 5.0
    context = {
        'product': product,
        'rating_range': ratings_range,
    }
    return render(request, 'products/product_detail.html', context)

# Add product view
@login_required
def product_add(request):

    """
    Display a form to add a new product and handle form submission.

    Only superusers are allowed to add new products. If the request method is 
    POST and the form is valid, the product is saved and the user is redirected 
    to the product list with a success message. Otherwise, the form is displayed.

    Returns:
        - Renders `product_add.html` with the form for GET requests.
        - Redirects to 'products' after successful form submission.
    """
    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to add products.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        # Check if the form is valid
        if form.is_valid():
            form.save()  # Save the new product
            messages.success(request, "Product added successfully.")
            return redirect('products')  # Redirect to the product list page
        else:
            # Log any errors
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "There was an error with the form. Please check the fields.")
    else:
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, 'products/product_add.html', context)

# delete product view
@login_required
def delete_product(request, pk):

    """
    Render a confirmation page before deleting a product.

    This view allows a superuser to delete a product. If the request is 
    a POST, the product is deleted and the user is redirected to the 
    product list with a success message. Otherwise, a confirmation page 
    is displayed.

    Only superusers can access this view.
    """

    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete products.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(models.Product, pk=pk)

    if request.method == 'POST':  # If user confirms deletion
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect(reverse('products'))

    context = {
        'product': product
    }
    return render(request, 'products/product_delete_confirmation.html', context)


# Update product view
@login_required
def product_update(request, pk):

    """
    Update an existing product.

    This view allows a superuser to edit product details. If the request is 
    a POST, the form is validated and saved. Otherwise, the form is displayed 
    with the current product data.

    Only superusers can access this view.
    """

    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to update products.')
        return redirect(reverse('home'))

    product = get_object_or_404(models.Product, pk=pk)

    # Handle form submission
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  
            messages.success(request, "Product updated successfully.")
            return redirect('product-detail', pk=product.id)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/product_update.html', context)


@login_required
def submit_product_rating(request, pk):
    """
    Allows an authenticated user to submit a rating and comment for a product.
    If the user has already rated the product, it updates the existing rating.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the product to rate.

    Returns:
        HttpResponse: Redirects back to the product detail page after submitting the rating.
    """
    product = get_object_or_404(models.Product, pk=pk)

    # Check if the user has already rated the product
    existing_rating = models.ProductRating.objects.filter(product=product, user=request.user).first()

    # If a rating already exists, update it
    if existing_rating:
        existing_rating.rating = request.POST.get('rating')
        existing_rating.comment = request.POST.get('comment')
        existing_rating.save()
        messages.success(request, "Your rating has been updated successfully.")
        
    else:
        # Otherwise, create a new rating
        models.ProductRating.objects.create(
            product=product,
            user=request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment'),
        )
        messages.success(request, "Thank you for your rating!")
    # Redirect back to the product detail page
    return redirect('product-detail', pk=product.pk)