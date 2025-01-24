from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from products.factories import ProductFactory

from users.factories import (
    AddressFactory, CartFactory, CartItemFactory,
    UserFactory, UserProfileFactory
)

User = get_user_model()


class PofileModelTest(TestCase):
    """Test Profile Model."""
    def setUp(self) -> None:
        """Prepare data"""
        self.user = UserFactory()
        self.profile = UserProfileFactory(
            user = self.user,
            mobile="9999999999",
            alternate_number="1111111111"
        )

    def test_create_profile(self):
        """Test profile creation."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.mobile, "9999999999")
        self.assertEqual(self.profile.alternate_number, "1111111111")
        self.assertIsNotNone(self.profile.created_at)
        self.assertIsNotNone(self.profile.updated_at)
        self.assertIsNone(self.profile.deleted_at)
        self.assertIsNone(self.profile.created_by)
        self.assertIsNone(self.profile.updated_by)
        self.assertIsNone(self.profile.deleted_by)

class AddressModelTest(TestCase):
    """Test for Address Model"""

    def setUp(self):
        """Prepare data for tests."""
        self.profile = UserProfileFactory()
        self.address = AddressFactory(
            profile = self.profile,
            address_line="101",
            near_by="test_near_by",
            city="test_city",
            state="test_state",
            country="test_country",
            pincode="121342",
            latitude="12475.0454",
            longitude="12451.1581"
        )
        return super().setUp()

    def test_create_address(self):
        """Test address creation."""
        self.assertEqual(self.address.profile, self.profile)
        self.assertEqual(self.address.address_line, "101")
        self.assertEqual(self.address.near_by, "test_near_by")
        self.assertEqual(self.address.city, "test_city")
        self.assertEqual(self.address.state, "test_state")
        self.assertEqual(self.address.country, "test_country")
        self.assertEqual(self.address.pincode, "121342")
        self.assertEqual(self.address.latitude, "12475.0454")
        self.assertEqual(self.address.longitude, "12451.1581")
        self.assertIsNotNone(self.address.created_at)
        self.assertIsNotNone(self.address.updated_at)
        self.assertIsNone(self.address.deleted_at)
        self.assertIsNone(self.address.created_by)
        self.assertIsNone(self.address.updated_by)
        self.assertIsNone(self.address.deleted_by)

class CartModelTest(TestCase):
    """Test Cart Model."""

    def setUp(self):
        """Prepare data for tests."""
        self.profile = UserProfileFactory()
        self.cart = CartFactory(
            profile = self.profile,
            ip_address="124.0.0.220"
        )
    
    def test_create_cart(self):
        """Test cart creation."""
        self.assertEqual(self.cart.profile, self.profile)
        self.assertEqual(self.cart.ip_address, "124.0.0.220")
        self.assertIsNotNone(self.cart.created_at)
        self.assertIsNotNone(self.cart.updated_at)
        self.assertIsNone(self.cart.deleted_at)
        self.assertIsNone(self.cart.created_by)
        self.assertIsNone(self.cart.updated_by)
        self.assertIsNone(self.cart.deleted_by)
    
class CartItemModelTest(TestCase):
    """Test CartItem Model."""

    def setUp(self):
        """Prepare data for tests."""
        self.cart = CartFactory()
        self.product = ProductFactory()
        self.cart_item = CartItemFactory(
            cart = self.cart,
            product=self.product,
            quantity=2,
        )
    
    def test_create_cart_item(self):
        """Test cart item creation."""
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.quantity, 2)
        # self.assertEqual(self.cart_item.product_price, self.product.price)
        self.assertEqual(
            self.cart_item.product_discounted_price,
            self.product.discounted_price
        )
        self.assertEqual(
            self.cart_item.total_price,
            self.product.discounted_price * self.cart_item.quantity
        )
        self.assertIsNotNone(self.cart_item.created_at)
        self.assertIsNotNone(self.cart_item.updated_at)
        self.assertIsNone(self.cart_item.deleted_at)
        self.assertIsNone(self.cart_item.created_by)
        self.assertIsNone(self.cart_item.updated_by)
        self.assertIsNone(self.cart_item.deleted_by)

class TestCartView(TestCase):
    """Test Cart View."""
    def setUp(self):
        """Prepare data for tests."""
        self.url = reverse('cart')
        self.client = Client()
        
    def test_cart_view(self):
        """Test cart view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/cart.html')
