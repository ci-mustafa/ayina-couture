from django.urls import path
from .views import quickcheckout

urlpatterns = [
    path('', quickcheckout, name='quickcheckout')
]