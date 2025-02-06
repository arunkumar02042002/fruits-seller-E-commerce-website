from decimal import Decimal

from django_ckeditor_5 import fields

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from common.models import BaseModel

from products.choices import (
    ProductCategoryChoice,
    QuantityTypeChoices,
    RatingChoices
)


User = get_user_model()


class Tag(BaseModel):
    title = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return "#" + self.title

    def clean(self) -> None:
        self.title = self.title.lower()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Product(BaseModel):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    description = fields.CKEditor5Field()
    category = models.CharField(max_length=10, choices=ProductCategoryChoice.choices)
    sub_category = models.CharField(max_length=15)
    discount_in_percent = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))]
    )
    stock = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.CharField(max_length=10, null=True, blank=True)
    unit = models.CharField(
        max_length=10,
        choices=QuantityTypeChoices.choices,
        default=QuantityTypeChoices.NOT_SET,
    )
    image = models.ImageField(
        upload_to="products/product_images", null=True, blank=True
    )
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.FIVE)
    is_featured = models.BooleanField(default=False)

    extra_info = models.JSONField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, through="ProductTag", related_name="products")

    @property
    def discounted_price(self):
        # Ensure that both price and discount_in_percent are Decimal
        price_decimal = Decimal(self.price)
        discount_decimal = Decimal(self.discount_in_percent)
        discounted_price = price_decimal * (1 - discount_decimal / Decimal(100))
        return round(discounted_price, 2)

    def __str__(self) -> str:
        return self.name

    def in_stock(self):
        """Check if the product is in stock"""
        return self.stock > 0

    def save(self, *args, **kwargs):
        if self.sub_category:
            self.sub_category = self.sub_category.lower()
        return super().save(*args, **kwargs)


class ProductTag(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True, blank=True
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_id", "tag_id"], name="unique_product_tag"
            )
        ]

    def __str__(self) -> str:
        return "Tag-" + str(self.tag_uuid) + "-product-" + str(self.product_uuid)


class Coupon(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    is_always_valid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    min_price_required = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00')
    )

    def __str__(self) -> str:
        return self.code

    def clean(self) -> None:
        self.code = self.code.upper()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    

class ProductReview(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="reviews"
    )
    profile = models.ForeignKey(
        'users.Profile', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="reviews"
    )
    review = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.FIVE)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return f"profile-{self.profile_id}-rating-{self.rating}"
    
    def save(self, *args, **kwargs):
        if self.email and self.profile is None:
            user = User.objects.filter(email=self.email).first()
            self.profile = user.profile if user else None
        return super().save(*args, **kwargs)
