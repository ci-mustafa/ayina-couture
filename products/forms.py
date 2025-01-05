from django import forms
from .models import Product


# Product form
class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.

    This form includes fields such as name, description, price, collection, material, 
    stock quantity, color, gender, occasion, featured status, size availability, and image. 
    It also applies Bootstrap styling to form inputs for better UI experience.

    Attributes:
        model (Product): The associated model for this form.
        fields (list): Specifies the fields to be included in the form.
        widgets (dict): Customizes form field widgets for better UI styling.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 
        'collection','material','stock_quantity',  
        'color', 'gender', 'occasion', 'is_featured',
        'has_sizes','image', 
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material'}),
            'has_sizes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'collection': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'occasion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occasion'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
        }
