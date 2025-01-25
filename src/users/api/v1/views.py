from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from common.responses import (
    response_204NoContent,
    reponse_200OK,
    reponse_201Created
)

from products.models import Product

from users.api.v1.permissions import IsCartItemOwner

from users.api.v1.serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)

from users.db_utils import get_cart_from_request_obj, get_cart_total
from users.models import Cart, CartItem


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
        return super().get_queryset().filter(
            ip_address=ip_address, profile__isnull=True
        ).prefetch_related('cart_items').first()
    
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


class CartItemAPIView(RetrieveUpdateDestroyAPIView):
    """Update cart items."""
    serializer_class = CartItemUpdateSerializer
    permission_classes = [IsCartItemOwner]
    queryset = CartItem.objects.all()
    lookup_field = 'uuid'
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return reponse_200OK(
            "Cart item retreived successfully.",
            payload = {
                **response.data
            }
        )
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return reponse_200OK(
            "Cart item updated successfully.",
            payload = {
                **response.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_204NoContent(
            "Cart item deleted successfully.",
        )

class CartTotalView(APIView):
    """Get total price of cart items."""
    def get(self, request):
        cart = get_cart_from_request_obj(request)
        sub_total = get_cart_total(cart)
        
        return reponse_200OK(
            "Cart total_price retreived successfully.",
            payload = {
                "sub_total": sub_total,
                "delivery_fee": Decimal(99.00),
                "total": sub_total + Decimal(99.00)
            }
        )