import uuid
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
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

    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_final_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Order creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

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
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderitems"
    )  # Links each item to an order with "orderitems" as related name
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )  # Links item to a product (null if product is deleted)
    size = models.CharField(max_length=10, null=True, blank=True)  # Optional size field
    quantity = models.PositiveIntegerField(default=1)  # Number of this product in the order
    order_item_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  

    def save(self, *args, **kwargs):
       
        self.order_item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

   


    
