from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from products.models import Product
from .models import Order, OrderItem
from cart.contexts import cart_context
from profiles.models import UserProfile
import stripe


def quickcheckout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'There is nothing in your cart at the moment!')
        return redirect('products')  # Redirect to product page or other relevant page

    current_cart = cart_context(request)
    total = current_cart['final_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Initialize form data for authenticated users
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        initial_data = {
            'full_name': user_profile.full_name,
            'email': user_profile.user.email,  # Get email from user model
            'phone_number': user_profile.phone_number,
            'country': user_profile.country,
            'postcode': user_profile.postcode,
            'city': user_profile.city,
            'street_address': user_profile.street_address,
        }
    else:
        initial_data = {}

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
            if request.user.is_authenticated and 'save-info' in request.POST:
                order.user = request.user
                # Update the user's profile with the order info
                user_profile.full_name = form_data['full_name']
                user_profile.phone_number = form_data['phone_number']
                user_profile.email = form_data['email']
                user_profile.country = form_data['country']
                user_profile.postcode = form_data['postcode']
                user_profile.city = form_data['city']
                user_profile.street_address = form_data['street_address']
                user_profile.save()
            # Save the order to the database
            order.user = request.user
            order.save()

            for key, item in cart.items():
                # Extract product ID from the key
                product_id = key.split('_')[0]
                product = Product.objects.get(id=product_id)
                quantity = item['quantity']
                size = item.get('size', '')

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
            # Capture form errors
            form_errors = " ".join([f"{field}: {' '.join(errors)}" for field, errors in order_form.errors.items()])
            
            # Display form errors in the message
            messages.error(request, f"There was an error with your form. Please double-check your information. — Errors: {form_errors}")



    order_form = OrderForm(initial=initial_data)
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