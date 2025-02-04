from django.urls import path
from .views import quickcheckout, checkout_success
from .webhooks import webhook
urlpatterns = [
    path('', quickcheckout, name='quickcheckout'),
    path('checkout_success/<order_number>', checkout_success, name='checkout-success'),
    path('wh/', webhook, name='webhook'),
]