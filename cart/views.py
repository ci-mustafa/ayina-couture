from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.contrib import messages
from products.models import Product



# cart view
def view_cart(request):
    return render(request, 'cart/cart.html')


# add item to the cart view
def add_to_cart(request, id):

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


def update_cart_item(request, id):
    product = get_object_or_404(Product, pk=id)
    cart = request.session.get('cart', {})
    
    if product.has_sizes:
        size = request.POST.get('size')
        cart_item_key = f"{id}_{size}"  
    else:
        cart_item_key = str(id)  

    if cart_item_key in cart:
        cart_item = cart[cart_item_key]
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', cart_item['quantity'])) 
            size = request.POST.get('size', cart_item['size'])  
            cart[cart_item_key]['quantity'] = quantity
            cart[cart_item_key]['size'] = size
            request.session['cart'] = cart
            messages.success(request, f'Cart item updated: {product.name}')
            return redirect('view-cart') 
    else:
        messages.error(request, "Cart item not found.")
        return redirect('view-cart') 
    return render(request, 'cart/update_cart_item.html', {
        'product': product, 
        'cart_item': cart_item,  
    })



def delete_cart_item(request, id, size=None):  
    cart = request.session.get('cart', {})
    cart_item_key = f"{id}_{size}" if size else str(id)

    if cart_item_key in cart:
        del cart[cart_item_key]
        request.session['cart'] = cart 
        messages.success(request, 'Item removed from cart')
    else:
        messages.error(request, 'Item not found in cart')
    return redirect('view-cart')





