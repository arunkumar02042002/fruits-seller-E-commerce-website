from decimal import Decimal

from django.db.models import Sum

from users.models import Cart

def get_cart_from_request_obj(request):
    """Return cart object from request object."""
    user = request.user
    ip_address = request.META.get('REMOTE_ADDR')
    if user.is_authenticated:
        return Cart.objects.filter(profile__user=user).first()
    return Cart.objects.filter(ip_address=ip_address, profile__isnull=True).first()
    

def get_cart_total(cart):
    """Return total price of items in cart."""
    sub_total = 0
    if cart is not None:
        sub_total = cart.cart_items.aggregate(
            sub_total=Sum('total_price')
        )['sub_total']
    
    return Decimal(sub_total) if sub_total else Decimal('0.00')