from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_context(request):
    """
    Context processor for cart details.

    This function calculates the total cost of items in the cart, 
    determines the applicable delivery cost, and checks if the user 
    qualifies for free delivery based on the threshold set in settings.

    Delivery is calculated as a percentage of the total order value unless 
    the order qualifies for free delivery.

    Returns:
        dict: A dictionary containing cart details, including:
            - cart_items (list): List of items in the cart.
            - total (Decimal): Total cost of items in the cart.
            - product_count (int): Number of products in the cart.
            - delivery (Decimal): Delivery cost based on order value.
            - free_delivery_delta (Decimal): Amount needed to qualify for free delivery.
            - free_delivery_threshold (Decimal): The minimum amount required for free delivery.
            - grand_total (Decimal): Final total including delivery costs.
    """
    
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    for key, item in cart.items():
        # Extract product ID from the composite key (if size is present)
        id = key.split('_')[0]  # This gives you the numeric product ID part
        quantity = item['quantity']  # Extract quantity from the cart item
        product = get_object_or_404(Product, pk=id)  # Query by the numeric product ID

        # Add the cost of this item to the total
        total += quantity * product.price  
        product_count += quantity  # Increment the product count

        cart_items.append({
            'id': id,
            'quantity': quantity,
            'product': product,
            'size': item.get('size')  # Include size if available
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
