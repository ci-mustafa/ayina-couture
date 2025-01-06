from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from products.models import Product



# cart view
def view_cart(request):
    return render(request, 'cart/cart.html')


# add item to the cart view
def add_to_cart(request, id):
    
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if id in list(cart.keys()):
        cart[id] += quantity
    else:
        cart[id] = quantity

    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect(redirect_url)



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

    print(request.session['cart'])
    
    return redirect(redirect_url)

