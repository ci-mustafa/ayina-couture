from django.db import models

# Create your models here.

class NewsletterSubscription(models.Model):
    """
    Model to store email subscriptions for the newsletter.

    Attributes:
        email (EmailField): The email address of the subscriber.
        subscribed_at (DateTimeField): The timestamp
        when the user subscribed.
    """

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
