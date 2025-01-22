import uuid

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.factories import CartFactory, CartItemFactory, UserProfileFactory
from products.factories import ProductFactory

class CartItemListAPIViewTests(APITestCase):
    """Test the CartItemListAPIView view."""
    def setUp(self):
        """Setup the test."""
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.cart = CartFactory(profile=self.profile, ip_address='127.0.0.1')
        CartItemFactory(cart=self.cart)
        self.url = reverse('cart-item-list')

    def test_get_cart_items_authenticated_user(self):
        """Test get cart items for authenticated user."""
        self.client.force_login(user=self.profile.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']['cart_items']), 1)

    def test_get_cart_items_guest_user(self):
        """Test get cart items for guest user."""
        CartItemFactory(cart=self.cart)
        response = self.client.get(self.url, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']['cart_items']), 2)

    def test_get_cart_items_no_cart(self):
        """Test get cart items for user with no cart."""
        response = self.client.get(self.url, REMOTE_ADDR='192.168.0.1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']['cart_items']), 0)

class CartItemCreateAPIViewTests(APITestCase):
    """Test the CartItemCreateAPIView view."""
    def setUp(self):
        self.client = APIClient()
        self.user = UserProfileFactory().user
        self.product = ProductFactory(name='Test Product', price=10.0)
        self.url = reverse('cart-item-create')

    def test_add_cart_item_authenticated_user(self):
        """Test add cart item for authenticated user."""
        self.client.force_login(self.user)
        data = {
            'product_uuid': self.product.uuid,
            'quantity': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product added to cart successfully.')
        self.assertEqual(response.data['payload']['product_uuid'], str(self.product.uuid))
        self.assertEqual(response.data['payload']['quantity'], 1)

    def test_add_cart_item_guest_user(self):
        """Test add cart item for guest user."""
        data = {
            'product_uuid': self.product.uuid,
            'quantity': 2
        }
        response = self.client.post(self.url, data, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product added to cart successfully.')
        self.assertEqual(response.data['payload']['product_uuid'], str(self.product.uuid))
        self.assertEqual(response.data['payload']['quantity'], 2)

    def test_add_cart_item_invalid_product(self):
        """Test add cart item with invalid product."""
        self.client.login(username='testuser', password='testpassword')
        data = {
            'product_uuid': uuid.uuid4(),
            'quantity': 1
        }
        response = self.client.post(self.url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
