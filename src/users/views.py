from django.views.generic import TemplateView

from users.models import Cart

# Create your views here.
class CartView(TemplateView):
    """Cart view."""
    template_name = 'users/cart.html'
