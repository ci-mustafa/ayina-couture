from django.db import models

# contact model
class Contact(models.Model):
    """
    A model representing a contact message.

    This model is used to store contact information and messages submitted
    by users through a contact form. It includes the user's name,
    email address, and the content of the message they wish to send.

    Attributes:
        name (CharField): The name of the person submitting the
        contact message.
        Limited to 60 characters.
        email (EmailField): The email address of the person submitting
        the message.
        Validates that the input is a properly formatted email address.
        message (TextField): The message content that the user wants to send.
        This is a free text field that can store long messages.
    """
    name = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.TextField()
