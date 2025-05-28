from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic import TemplateView

from orders.constants import SHIPPING_CHARGE

from users.db_utils import get_cart_from_request_obj
from users.models import Cart, CartItem

# Create your views here.
class CheckoutView(TemplateView):
    template_name = 'orders/checkout.html'
    queryset = Cart.objects.all()

    def get(self, request, *args, **kwargs):
        """Render checkout page."""
        cart = self.get_cart()
        if not cart or not cart.cart_items.exists():
            return redirect('cart')
        return render(request, self.template_name, self.get_context_data())

    def get_cart(self):
        """Fetch cart object from request."""
        return get_cart_from_request_obj(self.request)
    
    def get_cart_items(self):
        """Fetch cart object."""
        cart = self.get_cart()
        if cart:
            return cart.cart_items.all()
        return None
    
    def get_addresses(self):
        """Fetch addresses of the user."""
        user = self.request.user
        if user.is_authenticated:
            return user.profile.address_set.all()
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        context["cart"] = cart
        context["addresses"] = self.get_addresses()
        context["shipping_charges"] = SHIPPING_CHARGE
        context["cart_amount"] = cart.cart_amount
        context["payable_amount"] = (
            cart.cart_amount + SHIPPING_CHARGE
        ) if cart else 0.00
        return context


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'


class OrderFailureView(TemplateView):
    template_name = 'orders/order_failed.html'
