from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Wishlist



# wishlist view
@login_required
def list_wishlist(request):
    """
    Displays the wishlist of the logged-in user.

    This view retrieves all wishlist items associated with the current user
    and passes them to the template for rendering. Only logged-in users can
    access this view.

    Args:
        request: The HTTP request object containing the user information.

    Returns:
        A rendered template ('wishlist/wishlist.html') with the user's wishlist items.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context)


# Add to wishlist
@login_required
def add_to_wishlist(request, product_id):
    """
    Adds a product to the logged-in user's wishlist.

    This view checks if the product is already in the user's wishlist. If it is not,
    the product is added to the wishlist and a success message is shown. If the product
    is already in the wishlist, an informational message is displayed.

    Args:
        request: The HTTP request object containing the user information and optional
                 redirect URL.
        product_id: The ID of the product to be added to the wishlist.

    Returns:
        Redirects the user back to the product details page or the wishlist page, 
        based on the request data.
    """
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    if wishlist.products.filter(id=product.id).exists():
        messages.info(request, f"'{product.name}' is already in your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"'{product.name}' has been added to your wishlist!")
    return redirect(request.POST.get('redirect_url', 'list-wishlist'))



# Remove view
@login_required
def remove_wishlist_item(request, product_id):
    """
    Removes a product from the logged-in user's wishlist.

    This view checks if the product exists in the user's wishlist. If it does,
    it removes the product and displays a success message. If the product is not
    in the wishlist, an error message is displayed.

    Args:
        request: The HTTP request object that contains the user information.
        product_id: The ID of the product to be removed from the wishlist.

    Returns:
        Redirects the user back to the wishlist page after attempting to remove the product.
    """
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove the product from the user's wishlist
    if product in wishlist.products.all():
        wishlist.products.remove(product) 
        messages.success(request, f"{product.name} has been removed from your wishlist.")
    else:
        messages.error(request, "The item could not be found in your wishlist.")
    return redirect('list-wishlist') 


