from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from cart.contexts import cart_context
import stripe

def quickcheckout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'There is nothing in your cart at the moment!')
    

    current_cart = cart_context(request)
    total = current_cart['final_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            request.session['cart'] = {}  
            request.session.modified = True
            messages.success(request, "Your payment was successful! Your order has been placed.")
            return redirect('products')  

    order_form = OrderForm()
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'quickcheckout/quickcheckout.html', context)
