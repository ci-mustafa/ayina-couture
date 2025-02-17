import uuid
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """
    Represents an order placed by a user.
    Attributes:
        order_number (str): A unique identifier for the order.
        user (ForeignKey): The user who placed the order.
        full_name (str): The full name of the customer.
        email (str): The email address of the customer.
        phone_number (str): The phone number of the customer.
        country (str): The country where the order is being shipped.
        postcode (str): The postal code of the shipping address (optional).
        city (str): The city for the shipping address.
        street_address (str): The street address for delivery.
        status (str): The current status of the order
        (e.g., pending, paid, shipped).
        delivery_cost (Decimal): The cost of delivering the order.
        order_cost (Decimal): The total cost of the ordered items.
        order_final_total (Decimal): The total cost including delivery cost.
        created_at (DateTime): Timestamp for when the order was created.
        updated_at (DateTime): Timestamp for the last update to the order.

    Methods:
        _generate_order_number(): Generates a unique order number using UUID.
        update_total(): Updates the total cost of the order,
        including delivery cost.
        save(): Ensures an order number is generated before saving the order.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    order_number = models.CharField(max_length=32, null=False,
                                    editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address = models.CharField(max_length=80, null=False, blank=False)
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default='pending'
    )  # Order status tracking

    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                     null=False, default=0)
    order_final_total = models.DecimalField(max_digits=10,
                                            decimal_places=2, null=False,
                                            default=0)
    # Order creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()


    def update_total(self):
       
        # Calculate the total cost of all order items
        self.order_cost = self.orderitems.aggregate(
            total=Sum('order_item_total')
        )['total'] or 0  # Default to 0 if no items exist

        # Calculate delivery cost based on the threshold
        if self.order_cost < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_cost * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0

        # Calculate the final total including delivery cost
        self.order_final_total = self.order_cost + self.delivery_cost

        # Save the updated totals
        self.save()

    def save(self, *args, **kwargs):
        
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    """
    Represents a single item in an order.

    Attributes:
        order (ForeignKey): The order to which the item belongs.
        product (ForeignKey): The product associated with the
        order item (can be null if product is deleted).
        size (str): The size of the product (optional).
        quantity (int): The quantity of the product
        in the order (default is 1).
        order_item_total (Decimal): The total cost for the quantity
        of this item (calculated as product price * quantity).

    Methods:
        save(): Overrides the save method to calculate the total cost
        for the item before saving.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderitems"
    )  # Links each item to an order with "orderitems" as related name
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )  # Links item to a product (null if product is deleted)
    size = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    order_item_total = models.DecimalField(max_digits=10, decimal_places=2,
                                           editable=False)  

    def save(self, *args, **kwargs):
       
        self.order_item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

   


    
