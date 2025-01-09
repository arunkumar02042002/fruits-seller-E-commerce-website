from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal

from products.models import Tag, Product, ProductTag
from products.choices import ProductCategoryChoice
from products.factories import ProductFactory, TagFactory

from users.factories import UserFactory

User = get_user_model()


class TagModelTests(TestCase):
    def setUp(self):
        self.tag = TagFactory(title="Fresh")

    def test_tag_creation(self):
        self.assertEqual(self.tag.title, "fresh")
        self.assertIsNotNone(self.tag.created_at)
        self.assertIsNotNone(self.tag.updated_at)
        self.assertEqual(str(self.tag), "#fresh")

    def test_tag_uniqueness(self):
        with self.assertRaises(ValidationError):
            TagFactory(title="fresh").full_clean()

    def test_tag_clean(self):
        tag = Tag(title="EXAMPLE")
        tag.clean()
        self.assertEqual(tag.title, "example")


class ProductModelTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.tag = TagFactory()
        self.product = ProductFactory(
            name="Apple",
            description="Fresh Apple",
            category=ProductCategoryChoice.FRUIT,
            sub_category="Organic",
            price=Decimal("100.00"),
            discount_in_percent=Decimal("10.00"),
            created_by=self.admin_user,
        )
        self.product.tags.add(self.tag)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Apple")
        self.assertEqual(self.product.description, "Fresh Apple")
        self.assertEqual(self.product.category, ProductCategoryChoice.FRUIT)
        self.assertEqual(self.product.sub_category, "organic")
        self.assertEqual(self.product.price, Decimal("100.00"))
        self.assertEqual(self.product.discount_in_percent, Decimal("10.00"))

    def test_discounted_price(self):
        discounted_price = self.product.discounted_price
        self.assertEqual(discounted_price, Decimal("90.00"))

    def test_product_tag_relationship(self):
        self.assertEqual(self.product.tags.count(), 1)
        self.assertIn(self.tag, self.product.tags.all())

    def test_invalid_product_price(self):
        with self.assertRaises(ValidationError):
            invalid_product = Product(
                name="Orange",
                description="Orange",
                category="Fruit",
                sub_category="",
                price=Decimal("-50.00"),  # Invalid price
                discount_in_percent=Decimal("100.00"),
            )
            invalid_product.full_clean()

    def test_invalid_discount_price(self):
        with self.assertRaises(ValidationError):
            invalid_product = Product(
                name="Orange",
                description="Orange",
                category="Fruit",
                sub_category="",
                price=Decimal("50.00"),
                discount_in_percent=Decimal("-10.00"),  # Invalid
            )
            invalid_product.full_clean()

        with self.assertRaises(ValidationError):
            invalid_product = Product(
                name="Orange",
                description="Orange",
                category="Fruit",
                sub_category="",
                price=Decimal("50.00"),
                discount_in_percent=Decimal("101.00"),  # Invalid
            )
            invalid_product.full_clean()


class ProductTagModelTests(TestCase):
    """Tests for ProductTag Model"""

    def setUp(self):
        """Set up test data"""
        self.admin_user = UserFactory(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.tag = TagFactory(title="Organic")
        self.product = ProductFactory(
            name="Banana",
            description="Ripe Banana",
            category="Fruit",
            sub_category="organic",
            price=Decimal("50.00"),
            created_by=self.admin_user,
        )
        self.product_tag = ProductTag.objects.create(product=self.product, tag=self.tag)

    def test_product_tag_creation(self):
        """Test ProductTag Creation"""
        self.assertEqual(self.product_tag.product, self.product)
        self.assertEqual(self.product_tag.tag, self.tag)

    def test_unique_product_tag(self):
        """Test unique constraint violation"""
        with self.assertRaises(ValidationError):
            duplicate_product_tag = ProductTag(product=self.product, tag=self.tag)
            duplicate_product_tag.full_clean()
