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
            'full_name': forms.TextInput(attrs={'placeholder':
                                        'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder':
                                     'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'placeholder':
                                            'Enter your phone number'}),
            'country': forms.TextInput(attrs={'placeholder':
                                       'Enter your country'}),
            'postcode': forms.TextInput(attrs={'placeholder':
                                       'Enter your postcode'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'street_address': forms.TextInput(attrs={'placeholder': 
                                              'Enter your street address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iterate through all fields to apply customizations
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                # Append '*' to the field label for required fields
                field.label = f"{field.label} *"
            else:
                # Remove the 'required' attribute for non-required fields
                field.required = False