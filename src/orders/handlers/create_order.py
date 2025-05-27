"""Handler for creating an order."""
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F, Q, Sum

from rest_framework.exceptions import ValidationError

from common.razorpay_utils import razorpay_client

from orders.choices import OrderStatusChoices, PaymentMethodChoices
from orders.constants import SHIPPING_CHARGE
from orders.models import Order, ProductInOrder

from users.models import Address, Cart, Profile
from users.serializers import AddressSerializer, CreateUserSerializer


User = get_user_model()


class CreateOrders:
    """Handler for creating an order."""

    def __init__(self, request):
        """Initialize the CreateOrders handler."""
        self.request = request
        self.request_data = request.data if request.data else {}
        self.ip_address = request.META.get('REMOTE_ADDR', None)
        self.process_request_data()
        self.cart = self.get_cart()
        self.callback_url = 'http://' + str(get_current_site(self.request)) + "/orders/confirm/"

    def process_address(self):
        """Process the address data from the request."""
        address_id = self.request_data.get('address_id', None)
        address_data = self.request_data.get('address_data', {})

        if not any([address_id, address_data]):
            raise ValidationError("Either address_id or address_data must be provided.")

        if self.user.is_authenticated and address_id:
            address = Address.objects.filter(
                pk=address_id, profile=self.user.profile).first()
            if address is None:
                raise ValidationError("Invalid address id.")
            return address
        else:
            address_serializer = AddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            return address_serializer.save(profile=self.user.profile)

    def create_user(self):
        """Create a user if not authenticated."""
        # Logic to create a user if not authenticated
        # This is a placeholder; actual implementation may vary
        user_data = self.request_data.get('user_data', {})
        email = user_data.get('email', None)
        mobile_number = user_data.get('mobile_number', None)

        user = User.objects.filter(
            Q(email=email) | Q(mobile_number=mobile_number),
            is_active=False).first()

        if user:
            # If user exists, update the user data
            user_serializer = CreateUserSerializer(instance=user, data=user_data)
        else:
            user_serializer = CreateUserSerializer(data=user_data)

        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Ensure the user has a profile
        Profile.objects.get_or_create(user=user)
        return user

    def process_request_data(self):
        """Process the request data"""
        self.user = self.request.user if self.request.user.is_authenticated else self.create_user()
        self.address = self.process_address()

        if self.address is None:
            raise ValidationError("Shipping address is required to create an order.")

        # Save the cart with the user's profile
        cart = self.get_cart()
        if not cart.profile:
            cart.profile = self.user.profile
            cart.save()
        
        paynent_method = self.request_data.get('payment_method', None)
        if paynent_method not in PaymentMethodChoices.payment_method_list():
            raise ValidationError(
                f"Invalid payment method."
            )
        self.payment_method = paynent_method 

    def get_cart(self):
        """Get the cart associated with the user or IP address."""
        cart = None
        if self.user.is_authenticated:
            cart = Cart.objects.filter(
                profile=self.user.profile).first()        
        elif self.ip_address:
            cart = self.get_cart_by_ip()

        if cart is None:
            raise ValidationError(
                "No cart found for the user.")

        return cart

    def get_cart_by_ip(self):
        """Get the cart associated with the IP address."""
        return Cart.objects.filter(
            ip_address=self.ip_address,
            profile__isnull=True).first()

    def validate_cart_items(self):
        """Validate if the cart exists and has items."""      
        if self.cart.cart_items.count() == 0:
            raise ValidationError(
                "Cart is empty. Cannot create order.")

    def get_cart_items(self):
        """Get cart items."""
        self.validate_cart_items()
        return self.cart.cart_items.all()

    def add_product_to_order(self, cart_items, order):
        # Add products to the order
        for item in cart_items:
            ProductInOrder.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

    def create_order_on_razorpay(self, order):
        """Create an order on Razorpay."""
        razorpay_order_id = razorpay_client.create_order(
            original_amount=order.total_amount,
            receipt=order.order_id,
            notes={
                'profile_id': order.profile.uuid,
                'cart_id': self.cart.uuid,
                'order_amount': order.order_amount,
                'total_amount': order.total_amount,
            }
        )

        if not razorpay_order_id:
            raise ValidationError("Failed to create order on Razorpay.")
        
        order.razorpay_order_id = razorpay_order_id
        order.status = OrderStatusChoices.PLACED
        order.payment_method = PaymentMethodChoices.RAZORPAY
        order.save()

    def create_order(self, **kwargs):
        """Create an order from the cart."""
        cart_items = self.get_cart_items()
        cart = self.cart

        order_amount = cart_items.annotate(
            item_price = F('product__discounted_price') * F('quantity')
        ).aggregate(
            total_amount=Sum('item_price')
        )['total_amount']

        total_amount = order_amount + Decimal(SHIPPING_CHARGE)

        # Here you would typically create an order object
        order = Order.objects.create(
            profile=cart.profile,
            shipping_address=self.address,
            order_amount=order_amount,
            total_amount=total_amount,
        )

        # Add products to the order
        self.add_product_to_order(cart_items, order)

        # Set initial order status
        order.status = OrderStatusChoices.CREATED
        order.save()

        if self.payment_method == PaymentMethodChoices.COD:
            order.payment_method = PaymentMethodChoices.COD
            order.status = OrderStatusChoices.PLACED
            order.save()
            return {
                'order_id': order.uuid,
                'payment_method': PaymentMethodChoices.COD,
                'payable_amount': order.total_amount * 100,
            }

        # Create order on razorpay
        self.create_order_on_razorpay(order)

        context={
            'order_id': order.uuid,
            'callback_url':  self.callback_url,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'payable_amount': order.total_amount*100,
            'payment_method': PaymentMethodChoices.RAZORPAY,
        }
        return context
