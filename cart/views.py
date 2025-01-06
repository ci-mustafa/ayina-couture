from django.shortcuts import render



# cart view
def view_cart(request):
    return render(request, 'cart/cart.html')
