from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = (
        'full_name', 'email', 'phone_number', 
        'country', 'postcode', 'city', 'street_address',
    )

    list_display = ('full_name', 'email', 'phone_number', 
        'country', 'postcode', 'city', 'street_address',)
