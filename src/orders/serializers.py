from rest_framework import serializers

from orders.choices import PaymentMethodChoices

from users.serializers import AddressSerializer, CreateUserSerializer


class OrderSerializer(serializers.Serializer):
    """Serializer for the Order model."""

    address_data = AddressSerializer(required=False)
    user_data = CreateUserSerializer(required=False)
    payment_method = serializers.ChoiceField(
        choices=PaymentMethodChoices.choices
    )
    address_id = serializers.UUIDField(required=False)

    class Meta:
        fields = (
            'payment_method',
            'address_data',
            'user_data',
            'address_id',
        )
