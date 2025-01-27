from decimal import Decimal
import uuid

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
    description = models.TextField()
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
    quantity_type = models.CharField(
        max_length=10,
        choices=QuantityTypeChoices.choices,
        default=QuantityTypeChoices.NOT_SET,
    )
    image = models.ImageField(
        upload_to="products/product_images", null=True, blank=True
    )
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.FIVE)
    is_featured = models.BooleanField(default=False)

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