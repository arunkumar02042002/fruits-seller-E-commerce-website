import random
import uuid

from factory import Faker, LazyFunction, post_generation, SubFactory
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDecimal

from products.choices import ProductCategoryChoice
from products.models import Tag, Product


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
    created_by = SubFactory('users.factories.UserFactory')
    price = FuzzyDecimal(50, 500)
    discount_in_percent = FuzzyDecimal(10, 100)

    @post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags after the product is created."""
        if not create:
            return
        if extracted:
            # Add the given tags
            for tag in extracted:
                self.tags.add(tag)
