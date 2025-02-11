from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from products.models import Coupon, Product, ProductReview, Tag

from users.serializers import ProfileSerializer


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

class CheckCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)

    def validate_code(self, value):
        """Validate coupon code."""
        if not value.isalnum():
            raise serializers.ValidationError("Invalid coupon code.")
        
        value = value.upper()
        
        coupon = Coupon.objects.filter(
            Q(is_always_valid=True) |
            Q(valid_from__lte=timezone.now(), valid_to__gte=timezone.now()),
            code=value,
            active=True,
        )

        coupon = coupon.first()

        if coupon is None:
            raise serializers.ValidationError("Could not find coupon.")
        return coupon

class ProductReviewSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            "review", "rating", "profile", "created_at"
        )
