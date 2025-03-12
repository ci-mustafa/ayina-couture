from django.contrib import admin
from .models import NewsletterSubscription
# Register your models here.

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    readonly_fields = ['subscribed_at']
