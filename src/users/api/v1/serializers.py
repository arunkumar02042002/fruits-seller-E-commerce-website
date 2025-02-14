from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from users.models import Cart, CartItem

from products.api.v1.serializers import ProductSerializer
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    net_weight = serializers.CharField()

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

            # if cart is created with ip_address, then update the profile
            # and ip_address fields
            if not cart.profile or not cart.ip_address: 
                cart.profile = profile
                cart.ip_address = ip_address
                cart.save()

            cart_item = CartItem.objects.filter(cart=cart, product_id=product_uuid).first()

            if cart_item:
                raise serializers.ValidationError("Product already exists in cart.")

            CartItem.objects.create(
                cart=cart,
                product_id=product_uuid,
                quantity=self.validated_data.get('quantity'),
            )
        return cart

class CartItemUpdateSerializer(serializers.ModelSerializer):
    net_weight = serializers.CharField(read_only=True)

    class Meta:
        model = CartItem
        read_only_fields = [
            'cart', 'product',
            'product_price',
            'product_discounted_price',
            'discount', 'total_price',
            'net_weight'
        ]
        exclude = ['deleted_at', 'created_by', 'updated_by', 'deleted_by']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity cannot be less than 1. Try deleting the item instead."
            )
        return value
