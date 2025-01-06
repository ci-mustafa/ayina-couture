from django.shortcuts import redirect, get_object_or_404
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

    # Create a unique identifier for the cart item (including size if it exists)
    item_key = f"{id}_{size}" if size else f"{id}"

    # If item already exists in cart, update the quantity
    if item_key in cart:
        cart[item_key]['quantity'] += quantity
    else:
        # Add new item to the cart
        cart[item_key] = {
            'quantity': quantity,
            'size': size,  
        }

    request.session['cart'] = cart

    print(request.session['cart'])
    
    return redirect(redirect_url)

