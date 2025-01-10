from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def quickcheckout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'There is nothing in your cart at the moment!')
    
    order_form = OrderForm()
    context = {
        'order_form': order_form
    }

    return render(request, 'quickcheckout/quickcheckout.html', context)
