from django.shortcuts import redirect, get_object_or_404, render, reverse
from collections import OrderedDict
from django.contrib import messages
from products.models import Product, Color


# cart view
def view_cart(request):
    """ View cart content and render cart.html page """
    return render(request, 'cart/cart.html')


# Add to cart view
def add_to_cart(request, id):
    """
    Add a product to the shopping cart stored in the session.
    This view allows users to add a product to their cart with an optional
    size and color selection. If the product already exists in the cart,
    its quantity is incremented; otherwise, a new entry is created.
    The cart is saved in the session, ensuring that the user's cart
    persists across requests.
    Args:
        request (HttpRequest): The HTTP request object containing POST data
        (such as product quantity, size, and color).
        id (str): The ID of the product to be added to the cart.
    Returns:
        HttpResponseRedirect: Redirects the user to the specified URL
        (usually the cart page or product page).
    Behavior:
        - If the product has sizes, a unique key (product_id + size) is used
        to identify the cart item.
        - If the product has colors, the selected color is included in the key.
        - If the product already exists in the cart, its quantity is updated
        by adding the quantity from the POST request.
        - If the product is not in the cart, a new entry is created with the
        specified quantity, size, and color (if applicable).
        - The cart is stored in the session under the 'cart' key.
        - A success message is shown to the user after the product is added.
    Notes:
        - If the product does not have a size or color, those fields are
        omitted from the cart item.
        - If the user attempts to add a product to the cart that has
        color options, the color is required to be passed in the POST data.
        - If no redirect URL is provided in the POST data, the user will be
        redirected to the same page they came from.
    Example:
        - Product has no size or color: Cart item key will be the product ID.
        - Product has size but no color: Cart item key will be the product ID
        and size.
        - Product has both size and color: Cart item key will be
        the product ID, size, and color.
    """
    product = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('size') if product.has_sizes else None

    # Check if the product has a color selection
    if 'color' in request.POST and product.color:
        color_id = request.POST.get('color')
        color = get_object_or_404(Color, id=color_id)
    else:
        color = None  # No color selected or product has no color option

    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Create a unique key by combining the product id, size (if applicable),
    # and color (if applicable)
    if product.has_sizes and size:
        if color:
            product_key = f"{id}_{size}_{color}"
        else:
            product_key = f"{id}_{size}"
    else:
        product_key = f"{id}"
    if product_key in cart:
        cart[product_key]['quantity'] += quantity
    else:
        cart[product_key] = {
            'quantity': quantity,
            'size': size,
            'color': color.name if color else None,
        }

    # Save the updated cart in the session
    request.session['cart'] = cart

    # Add success message
    messages.success(
        request,
        f'Item "{product.name}" has been successfully added to your cart.')
    return redirect(redirect_url)


# Update view
def update_cart_item(request, id, size=None, color=None):
    """
    Update the quantity, size, and color of a cart item.

    This view allows users to update the quantity, size, and color
    of an item already in their shopping cart.
    It retrieves the product using its ID, checks if the item
    exists in the cart, and processes the update.
    Args:
        request (HttpRequest): The HTTP request object containing
        the cart and form data.
        id (str): The ID of the product to be updated in the cart.
        size (str, optional): The size of the item to update, if applicable.
        color (str, optional): The color of the item to update, if applicable.
    Returns:
        HttpResponse: Redirects to the cart view upon successful update,
        or renders the update page if the item is found.

    Raises:
        Http404: If the product is not found in the database
        (via `get_object_or_404`).
    """
    # Get the product from the database using the provided product id
    product = get_object_or_404(Product, pk=id)
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})
    cart = OrderedDict(cart)

    # Construct the key for the cart item based on size and color
    if size and color:
        old_cart_item_key = f"{id}_{size}_{color}"
    elif size:
        old_cart_item_key = f"{id}_{size}"
    else:
        old_cart_item_key = str(id)

    # Check if the cart item exists using the constructed key
    if old_cart_item_key not in cart:
        messages.error(request, "Cart item not found.")
        return redirect('view-cart')

    # Get the cart item based on the constructed key
    cart_item = cart[old_cart_item_key]

    # Handle the POST request to update the cart item
    if request.method == 'POST':
        # Get the new quantity, size, and color from the form
        quantity = int(request.POST.get('quantity', cart_item['quantity']))
        new_size = request.POST.get('size', cart_item.get('size'))
        new_color = request.POST.get('color', cart_item.get('color'))

        # Ensure that the quantity is valid
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('view-cart')

        # Construct the new key for the cart item with updated size and color
        if new_size and new_color:
            new_cart_item_key = f"{id}_{new_size}_{new_color}"
        elif new_size:
            new_cart_item_key = f"{id}_{new_size}"
        else:
            new_cart_item_key = str(id)

        # Remove the old cart item key if it differs from the new key
        if old_cart_item_key != new_cart_item_key:
            del cart[old_cart_item_key]

        # Update the cart with the new values
        cart[new_cart_item_key] = {
            "quantity": quantity,
            "size": new_size if product.has_sizes else None,
            "color": new_color
        }

        # Save the updated cart back to the session
        request.session['cart'] = dict(cart)
        request.session.modified = True

        messages.success(request, f'Cart item updated: {product.name}')
        return redirect('view-cart')

    # Render the update page with the necessary information
    return render(request, 'cart/update_cart_item.html', {
        'product': product,
        'cart_item': cart.get(old_cart_item_key),
        'size': size,
        'color': color,
    })


# Delete cart item view
def delete_cart_item(request, id, size=None, color=None):
    """
    Remove an item from the cart.
    This view deletes a specific item from the cart, either with
    or without a size or color.
    If the item exists in the session-based cart,
    it is removed; otherwise, an error message is displayed.
    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The product ID of the item to be removed.
        size (str, optional): The size of the item (if applicable).
        color (str, optional): The color of the item (if applicable).

    Returns:
        HttpResponseRedirect: Redirects the user to the cart view with
        a success or error message.
    """
    cart = request.session.get('cart', {})

    # Construct the key based on size and color
    if size and color:
        cart_item_key = f"{id}_{size}_{color}"
    elif size:
        cart_item_key = f"{id}_{size}"
    else:
        cart_item_key = str(id)

    # Attempt to delete the item from the cart
    if cart_item_key in cart:
        del cart[cart_item_key]
        request.session['cart'] = cart  # Save the updated cart
        messages.success(request, 'Selected item removed from cart.')
    else:
        messages.error(request, 'Item not found in cart.')

    return redirect('view-cart')


# Delete all items from the cart
def delete_all_cart_items(request):
    """
    Removes all items from the cart.
    This view will clear the entire cart by removing all items
    stored in the session-based cart.
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the cart view
        with a success message.
    """
    # Clear the cart by resetting it
    request.session['cart'] = {}
    # Provide feedback to the user
    messages.success(request, 'All items have been removed from your cart.')
    # Redirect back to the cart view
    return redirect('view-cart')





