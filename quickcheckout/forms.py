from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number', 
            'country', 'postcode', 'city', 'street_address',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter your country'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Enter your postcode'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'street_address1': forms.TextInput(attrs={'placeholder': 'Enter your street address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # Mark all fields as required except 'postcode'
            field.required = True
            if field.name == 'postcode':
                field.required = False  # Make 'postcode' field optional
            # Add a '*' symbol for required fields
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.label = f"{field.label} *"