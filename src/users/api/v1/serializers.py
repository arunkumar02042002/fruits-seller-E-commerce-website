from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from users.models import Cart, CartItem

from products.api.v1.serializers import ProductSerializer
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        exclude = [
            'deleted_at', 'created_by',
            'updated_by', 'deleted_by'
        ]

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['cart_items']

class AddToCartSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def save(self, **kwargs):
        product_uuid = self.validated_data.get('product_uuid')
        profile = kwargs.get('profile')
        ip_address = kwargs.get('ip_address')

        with transaction.atomic():
            # nowait=True directly raises an error if the object is locked
            cart = (
                Cart.objects.filter(profile=profile) or
                Cart.objects.filter(ip_address=ip_address)
            ).select_for_update(nowait=True).first()

            if not cart:
               cart = Cart.objects.create(ip_address=ip_address, profile=profile)

            cart_item = CartItem.objects.filter(cart=cart, product_id=product_uuid).first()

            if cart_item:
                raise serializers.ValidationError("Product already exists in cart.")

            CartItem.objects.create(
                cart=cart,
                product_id=product_uuid,
                quantity=self.validated_data.get('quantity'),
            )
        return cart
