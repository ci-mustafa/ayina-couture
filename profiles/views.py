from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from quickcheckout.models import Order

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Failed to update profile. Please check the form for errors.')
    form = UserProfileForm(instance=profile)
    orders = profile.user.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'We’ve already confirmed your order number {order_number}. \
        A confirmation email was sent to you on the day you placed the order.'
    ))

    template = 'quickcheckout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
