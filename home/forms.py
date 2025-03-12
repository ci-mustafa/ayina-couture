from django import forms
from .models import NewsletterSubscription

class NewsletterForm(forms.ModelForm):
    """
    A form for subscribing to the newsletter.

    This form is based on the `NewsletterSubscription` model
    and allows users to
    enter their email addresses for subscription.
    It includes only the 'email' field.

    Meta:
        model (NewsletterSubscription):
        The model associated with this form.
        fields (list): Specifies that only the 'email' field
        is included in the form.
    """
    class Meta:
        model = NewsletterSubscription
        fields = ['email']