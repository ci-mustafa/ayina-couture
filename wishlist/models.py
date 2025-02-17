from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Wishlist model
class Wishlist(models.Model):
    """
    Represents a user's wishlist, storing products they are interested in.

    Attributes:
        user (OneToOneField): The user who owns the wishlist.
        products (ManyToManyField): A list of products added to
        the user's wishlist.
        created_at (DateTimeField): The timestamp when
        the wishlist was created.

    Methods:
        __str__(): Returns a string representation of the wishlist,
        showing the username of the owner.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
    

 


