import random
import uuid

from django.utils import timezone

from factory import Faker, LazyFunction, post_generation, Sequence
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDecimal

from products.choices import ProductCategoryChoice, QuantityTypeChoices
from products.models import Coupon, Product, ProductReview, Tag 

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = Faker("word", locale="en_US")

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    uuid = LazyFunction(uuid.uuid4)
    name = Faker('word')
    description = Faker('paragraph')
    category = LazyFunction(
        lambda: random.choice([choice[0] for choice in ProductCategoryChoice.choices])
    )
    sub_category = Faker('word')
    discount_in_percent = LazyFunction(lambda: round(random.uniform(0, 50), 2))
    image = ImageField(color="blue")
    price = FuzzyDecimal(50, 500)
    discount_in_percent = FuzzyDecimal(10, 100)
    quantity = 1
    unit = QuantityTypeChoices.KG

    @post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags after the product is created."""
        if not create:
            return
        if extracted:
            # Add the given tags
            for tag in extracted:
                self.tags.add(tag)


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = Sequence(lambda n: f"code{n}")
    discount = FuzzyDecimal(10, 100)
    is_always_valid = False
    valid_from = LazyFunction(lambda: timezone.now())
    valid_to = LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))
    active = True

class ProductReviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductReview

    rating = FuzzyDecimal(1, 5)
    review = Faker('paragraph')
