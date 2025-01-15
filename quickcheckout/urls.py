from django.urls import path
from .views import quickcheckout, checkout_success

urlpatterns = [
    path('', quickcheckout, name='quickcheckout'),
    path('checkout_success/<order_number>', checkout_success, name='checkout-success'),
]