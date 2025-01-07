from django.shortcuts import redirect, get_object_or_404, render, reverse
from collections import OrderedDict
from django.contrib import messages
from products.models import Product



# cart view
def view_cart(request):
    return render(request, 'cart/cart.html')


# add item to the cart view
def add_to_cart(request, id):

    """
    Add a product to the shopping cart stored in the session.

    This view allows users to add a product to their cart with an optional 
    size selection. If the product already exists in the cart, its quantity 
    is incremented; otherwise, a new entry is created.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.
        id (str): The ID of the product to be added.

    Returns:
        HttpResponseRedirect: Redirects the user to the specified URL.

    Behavior:
        - If the product has sizes, a unique key (product_id + size) is used.
        - If the item exists in the cart, the quantity is updated.
        - If the item is new, it is added to the cart.
        - The session is updated with the modified cart.
    """
    product = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('size') if product.has_sizes else None
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Create a unique key by combining the product id and size (if applicable)
    if product.has_sizes and size:
        product_key = f'{id}_{size}'  # Use product id and size as the key
    else:
        product_key = str(id)  # Use only the product id as the key if no size

    if product_key in cart:
        # If the product (with size) is already in the cart, increment the quantity
        cart[product_key]['quantity'] += quantity
    else:
        # If the product (with size) is not in the cart, add it with the current quantity and size
        cart[product_key] = {
            'quantity': quantity,
            'size': size,
        }

    request.session['cart'] = cart
    return redirect(redirect_url)


# Upate cart item view
def update_cart_item(request, id, size=None):

    """
    Update the quantity and size (if applicable) of an item in the cart.

    This view allows users to modify the quantity and/or size of an existing 
    product in their session-based cart. If the size changes, the item is 
    reassigned a new key in the cart dictionary.

    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The product ID of the item to be updated.
        size (str, optional): The current size of the item, if applicable. Defaults to None.

    Returns:
        HttpResponseRedirect: Redirects to the cart view upon successful update.
        HttpResponse: Renders the update cart item page if the item is found.

    Behavior:
        - If the item does not exist in the cart, an error message is displayed.
        - If a new size is selected, the old item entry is removed and a new one is created.
        - The cart order is preserved using OrderedDict.
    """
    # Fetch the product from the database using the product id
    product = get_object_or_404(Product, pk=id)

    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # Convert cart to OrderedDict to maintain order
    cart = OrderedDict(cart)

    # Determine the old cart item key
    old_cart_item_key = f"{id}_{size}" if size else str(id)

    # Check if the item exists in the cart before processing
    if old_cart_item_key not in cart:
        messages.error(request, "Cart item not found.")
        return redirect('view-cart')

    cart_item = cart[old_cart_item_key]  # Get existing item without popping it

    if request.method == 'POST':
        # Get new quantity and size from form
        quantity = int(request.POST.get('quantity', cart_item['quantity']))
        new_size = request.POST.get('size', cart_item.get('size'))  # Keep old size if not changed

        # Ensure quantity is valid
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('view-cart')

        # Create a new cart key based on the updated size
        new_cart_item_key = f"{id}_{new_size}" if new_size else str(id)

        # Remove the old entry only if the key changes
        if old_cart_item_key != new_cart_item_key:
            del cart[old_cart_item_key]

        # Update the cart item
        cart[new_cart_item_key] = {
            "quantity": quantity,
            "size": new_size if product.has_sizes else None
        }

        # Save the updated cart back to the session (convert back to dict)
        request.session['cart'] = dict(cart)
        request.session.modified = True  # Ensure session updates

        messages.success(request, f'Cart item updated: {product.name}')
        return redirect('view-cart')

    # Render the update page
    return render(request, 'cart/update_cart_item.html', {
        'product': product,
        'cart_item': cart.get(old_cart_item_key, cart_item),
        'size': size,
    })





# Delete cart item view
def delete_cart_item(request, id, size=None):  
    """
    Remove an item from the cart.

    This view deletes a specific item from the cart, either with or without a size.
    If the item exists in the session-based cart, it is removed; otherwise, an error message is displayed.

    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The product ID of the item to be removed.
        size (str, optional): The size of the item (if applicable). Defaults to None.

    Returns:
        HttpResponseRedirect: Redirects the user to the cart view with a success or error message.
    """
    cart = request.session.get('cart', {})
    cart_item_key = f"{id}_{size}" if size else str(id)

    if cart_item_key in cart:
        del cart[cart_item_key]
        request.session['cart'] = cart 
        messages.success(request, 'Item removed from cart')
    else:
        messages.error(request, 'Item not found in cart')
    return redirect('view-cart')





