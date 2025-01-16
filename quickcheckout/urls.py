from django.urls import path
from .views import quickcheckout, checkout_success, cache_checkout_data
from . import webhooks
urlpatterns = [
    path('', quickcheckout, name='quickcheckout'),
    path('checkout_success/<order_number>', checkout_success, name='checkout-success'),
    path('cache_checkout_data/', cache_checkout_data, name='cache-checkout-data'),
    path('wh/', webhooks.webhook, name='webhook'),
]