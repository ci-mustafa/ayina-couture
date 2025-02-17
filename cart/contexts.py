from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_context(request):
    """
    Context processor for cart details, including calculation of
    totals, delivery, and free delivery eligibility.
    This function calculates the total cost of items in the cart,
    determines the applicable delivery cost and checks if the user
    qualifies for free delivery based on a threshold set in the settings.
    Delivery is calculated as a percentage of the total order value unless
    the order qualifies for free delivery.
    The final total includes the cost of the items plus any
    applicable delivery charges.
    Args:
        request (HttpRequest): The HTTP request object,
        which includes the user's cart stored in the session.
    Returns:
        dict: A dictionary containing cart details, including:
            - cart_items (list): A list of dictionaries containing details
            about each item in the cart:
                - id (str): Product ID.
                - quantity (int): Quantity of the product.
                - product (Product): Product object.
                - size (str or None): Size of the product (if applicable).
                - color (str or None): Color of the product (if applicable).
                - subtotal (Decimal): Subtotal cost for the product
                (quantity * price).
            - total (Decimal): Total cost of all items in the cart
            (before delivery).
            - product_count (int): Total number of individual products in
            the cart.
            - delivery (Decimal): Delivery cost based on the total order value.
            Calculated as a percentage unless the order qualifies for
            free delivery.
            - free_delivery_delta (Decimal): Amount needed to qualify for
            free delivery, calculated based on the total order value.
            - free_delivery_threshold (Decimal): The minimum total required
            to qualify for free delivery (from settings).
            - final_total (Decimal): Final total including delivery costs.

    Notes:
        - The delivery cost is calculated as a percentage of the total order
        value based on `STANDARD_DELIVERY_PERCENTAGE` from settings.
        - If the total cart value is below the threshold for free delivery
        (`FREE_DELIVERY_THRESHOLD`), a delivery fee is applied.
        - If the total cart value is above or equal to the
        free delivery threshold, no delivery fee is applied.
        - `cart_items` includes details for each cart item such as product,
        quantity, size, color, and subtotal.
    """
    
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    for key, item in cart.items():
        # Extract product ID from the composite key (if size is present)
        id = key.split('_')[0]  # This gives you the numeric product ID part
        quantity = item['quantity']  # Extract quantity from the cart item
        product = get_object_or_404(Product, pk=id)
        subtotal = quantity * product.price
        # Add the cost of this item to the total
        total += quantity * product.price
        product_count += quantity  # Increment the product count
        cart_items.append({
            'id': id,
            'quantity': quantity,
            'product': product,
            'size': item.get('size'),  # Include size if available
            'color': item.get('color'),  # Add color to the cart item context
            'subtotal': subtotal,
        })
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    final_total = delivery + total
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'final_total': final_total,
    }

    return context
