from django.contrib import admin
from .models import Contact



# Contact admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'message'
    ]
