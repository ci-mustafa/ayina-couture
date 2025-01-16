from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from products.models import Product
from .models import Order, OrderItem
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
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'street_address': request.POST['street_address'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # Set the user field if the user is authenticated
            if request.user.is_authenticated:
                order.user = request.user
            else:
                messages.error(request, 'You must be logged in to place an order.')
                return redirect('account_login') 
            # Save the order to the database
            order.save()

            for key, item in cart.items():
                # Extract product ID from the key 
                product_id = key.split('_')[0]  
                product = Product.objects.get(id=product_id)
                quantity = item['quantity']
                size = item['size']

                # Create and save the order item
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    size=size  
                )
                order_item.save()

            # Save delivery info if user opts in
            request.session['save_info'] = 'save-info' in request.POST

            # Clear the cart, set success message, and redirect
            request.session['cart'] = {}
            request.session.modified = True
            return redirect(reverse('checkout-success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')


    order_form = OrderForm()
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'quickcheckout/quickcheckout.html', context)



def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Your payment was successful! Your order has been placed. \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'quickcheckout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)