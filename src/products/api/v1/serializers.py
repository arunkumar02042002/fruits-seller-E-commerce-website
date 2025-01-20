from rest_framework import serializers

from products.models import Product, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("title", "created_at", "updated_at")


class ProductSerializer(serializers.ModelSerializer):

    discounted_price = serializers.ReadOnlyField()
    discount = serializers.DecimalField(
        source='discount_in_percent',
        max_digits=4,
        decimal_places=2
    )
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        exclude = (
            "created_by", "updated_by",
            "deleted_at", "deleted_by"
        )
