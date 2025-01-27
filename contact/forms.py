from django import forms
from . import models


# contact form
class ContactForm(forms.ModelForm):
    """
    A form for submitting contact information, including name, email,
    and message.

    This form is based on the Contact model and includes custom
    widgets for each field with placeholders and Bootstrap form-control
    classes.
    The field labels are set to empty strings for a cleaner form appearance.
    """
    class Meta:
        model = models.Contact
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Your Name',
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Your Email',
            'class': 'form-control',
        })
        self.fields['message'].widget.attrs.update({
            'placeholder': 'Your Message',
            'class': 'form-control',
        })

        # Set labels to empty strings
        self.fields['name'].label = ''
        self.fields['email'].label = ''
        self.fields['message'].label = ''