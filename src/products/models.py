from decimal import Decimal
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from common.models import BaseModel

from products.choices import ProductCategoryChoice, RatingChoices


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
    image = models.ImageField(
        upload_to="products/product_images", null=True, blank=True
    )
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.FIVE)
    is_featured = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through="ProductTag", related_name="products")

    @property
    def discounted_price(self):
        return round(self.price * (1 - self.discount_in_percent/100), 2)

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
