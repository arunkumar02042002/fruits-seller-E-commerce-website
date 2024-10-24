import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from .choices import ProductCategoryChoice

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "#" + self.title

    def clean(self) -> None:
        self.title = self.title.lower()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=ProductCategoryChoice.choices)
    sub_category = models.CharField(max_length=15)
    discount_in_percent = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        upload_to="products/product_images", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    admin_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, through="ProductTag", related_name="products")

    @property
    def discounted_price(self):
        return self.price - ((self.price / 100) * self.discount_in_percent)

    def __str__(self) -> str:
        return str(self.admin_user_id) + "-" + self.name

    def save(self, *args, **kwargs):
        if self.sub_category:
            self.sub_category = self.sub_category.lower()
        return super().save(*args, **kwargs)


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_id", "tag_id"], name="unique_product_tag"
            )
        ]

    def __str__(self) -> str:
        return "Tag-" + str(self.tag_id) + "-product-" + str(self.product_id)
