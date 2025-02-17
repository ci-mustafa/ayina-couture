import uuid
from django.db import models
from typing import Optional
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


# Collection model
class Collection(models.Model):
    """
    Represents a collection of items in the application.
    Attributes:
    - title (str): The title of the collection,
    typically used for internal identification.
    - display_name (str): A user-friendly name for the collection,
    which can be shown to users in the UI.
    
    Methods:
        __str__(self):
            Returns the title of the collection as its string representation.
        return_display_name(self):
            Returns the display name of the collection if available;
            otherwise, returns None.
    """

    title = models.CharField(max_length=254, null=False, blank=False)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the collection object.
        """
        return self.title
    
    def return_display_name(self) -> str:
        """
        Returns the user-friendly display name of the collection.
        """
        return self.display_name


# Color model
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # Hex code for color
    color_code = models.CharField(max_length=7, unique=True)
    
    def __str__(self):
        return self.name


# Product model
class Product(models.Model):

    """
    Represents a product in the store, which could be
    a clothing item or accessory.
    Attributes:
    - collection: A foreign key to the Collection model,
    representing the collection the product belongs to (e.g., Summer, Winter).
    - sku: A unique identifier for the product, 
    typically used for inventory management.
    - name: The name of the product.
    - description: A detailed description of the product.
    - material: The material the product is made from (e.g., Cotton, Leather).
    - price: The price of the product.
    - has_sizes: A boolean indicating whether the product has
    different sizes available.
    - color: The color of the product, selected from related model.
    - occasion: Optional field to specify the occasion for which
        the product is suitable (e.g., Casual, Formal).
    - stock_quantity: The quantity of the product available in stock.
    - is_featured: A boolean indicating whether the product is featured
    on the website.
    - image_url: The URL for an image of the product.
    - image: A file field to store the image of the product.
    - created_at: The timestamp when the product was created.
    - updated_at: The timestamp when the product was last updated.
    
    Methods:
    - __str__: Returns the name of the product as a string representation.
    - is_in_stock: Returns a boolean indicating whether
        the product is in stock (stock_quantity > 0).
    - average_rating: Returns the average rating of the product,
    or `None` if no ratings exist.
    """

    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    sku = models.CharField(max_length=254, unique=True, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    material = models.CharField(max_length=254)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    color = models.ManyToManyField(Color, related_name='products', blank=True)
    occasion = models.CharField(max_length=254, null=True, blank=True) 
    stock_quantity = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self) -> str:
        """
        Returns the string representation of the Product instance.
        """
        return self.name

    @property
    def is_in_stock(self) -> bool:
        """
        Checks if the product is in stock.

        This property checks whether the product's stock
        quantity is greater than zero. It returns `True` if the
        product is available (stock_quantity > 0),
        and `False` if the product is out of stock (stock_quantity <= 0).

        Returns:
            bool: `True` if the product is in stock, `False` otherwise.
        """
        return self.stock_quantity > 0
    
    @property
    def average_rating(self) -> Optional[float]:
        """
        Calculates the average rating for the product.
        This property calculates the average rating for a
        product by gathering all associated ratings, summing them up,
        and dividing by the total number 
        of ratings. If no ratings exist, it returns `None`.

        Returns:
            float or None: The average rating of the product,
            or `None` if no ratings exist.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            total_ratings = sum([rating.rating for rating in ratings])
            return total_ratings / ratings.count()
        return None

    def save(self, *args, **kwargs) -> None:

        """
        Save method override for the Product model.

        This method ensures that an SKU (Stock Keeping Unit)
        is automatically generated if one is not already provided.
        It calls the `generate_sku` method to create a 
        unique SKU before saving the product instance.
        Returns:
        None
        """
        if not self.sku:  # Only generate if SKU is not already set
            self.sku = self.generate_sku()
        super(Product, self).save(*args, **kwargs)
    
    def generate_sku(self) -> str:

        """
        Generate a unique SKU for the product.

        This method generates an SKU using a random UUID, ensuring uniqueness. 
        The SKU follows the format: 'PROD-XXXXXXXX', where 'XXXXXXXX' is an 
        8-character uppercase hexadecimal string derived from the UUID.

        Returns:
        str: A string representing the generated SKU.
        """
        return f"PROD-{uuid.uuid4().hex[:8].upper()}"


# Productrating model
class ProductRating(models.Model):

    """
    Represents a rating given by a user to a product.
    This model stores a user's rating for a specific product.
    Each user can only rate a product once. Ratings are given on a
    scale from 1 to 5, and are associated with a product and
    the user who submitted the rating.
    Attributes:
    - product (ForeignKey): The product being rated,
    associated via a foreign key.
    - user (ForeignKey): The user who provided the rating,
    associated via a foreign key.
    - rating (DecimalField): The rating given by the user,
    ranging from 1 to 5.
    - created_at (DateTimeField): The timestamp when the rating was created.
    Methods:
        __str__: Returns a string representation of the rating,
            showing the product name and the user's username.
    """
    product = models.ForeignKey(Product, 
                                related_name='ratings', 
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.CharField(max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        """
        Metadata for the ProductRating model.

        Ensures that each user can only rate a product once by
        enforcing a unique constraint
        on the combination of `product` and `user`.
        """
        # Ensure a user can only rate a product once
        unique_together = ['product', 'user']
    
    def __str__(self):

        """
        Returns a string representation of the ProductRating instance.
        This method returns a string that represents the rating for a
        specific product by a specific user.

        Returns:
            str: A string in the format 
            "Rating for <product_name> by <user_username>"
        """
        return f"Rating for {self.product.name} by {self.user.username}"

