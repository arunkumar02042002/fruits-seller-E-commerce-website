from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveAPIView, CreateAPIView

from common.responses import reponse_200OK, reponse_201Created

from products.models import Product

from users.api.v1.serializers import (
    AddToCartSerializer,
    CartSerializer,
    CartItemSerializer
)
from users.models import Cart

class CartItemListAPIView(RetrieveAPIView):
    """Fetch cart items for authenticated user or guest user."""
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_object(self):
        """Fetch cart object."""
        user = self.request.user
        ip_address = self.request.META.get('REMOTE_ADDR')
        if user.is_authenticated:
            return super().get_queryset().filter(profile__user=user).prefetch_related('cart_items').first()
        return super().get_queryset().filter(ip_address=ip_address).prefetch_related('cart_items').first()
    
    def get(self, request, *args, **kwargs):
        """Get cart items for authenticated user or guest user."""
        response = super().get(request, *args, **kwargs)
        return reponse_200OK(
            "Cart items retreived successfully.",
            payload = {
                "cart_items": response.data["cart_items"]
            }
        )
    
class CartItemCreateAPIView(CreateAPIView):
    """Add product to cart."""
    serializer_class = AddToCartSerializer
    detail_serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        product_uuid = request.data.get('product_uuid')
        get_object_or_404(Product, uuid=product_uuid)
        response = super().post(request, *args, **kwargs)
        return reponse_201Created(
            "Product added to cart successfully.",
            payload = {
                **response.data
            }
        )

    def perform_create(self, serializer):
        user = self.request.user
        ip_address = self.request.META.get('REMOTE_ADDR')

        if user.is_authenticated:
            serializer.save(profile=user.profile, ip_address=ip_address)
        else:
            serializer.save(ip_address=self.request.META.get('REMOTE_ADDR'))
