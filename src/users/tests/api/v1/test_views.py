import uuid
from decimal import Decimal

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from products.factories import ProductFactory

from users.choices import AddressChoices
from users.factories import (
    AddressFactory, CartFactory,
    CartItemFactory, UserProfileFactory
)


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
        cart = CartFactory(ip_address='220.0.01.2', profile=None)
        CartItemFactory(cart=cart)
        response = self.client.get(self.url, REMOTE_ADDR='220.0.01.2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']['cart_items']), 1)

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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CartItemAPIViewTests(APITestCase):
    """Test the CartItemUpdateAPIView view."""
    def setUp(self):
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.cart = CartFactory(
            profile=self.profile,
            ip_address='127.0.0.1'
        )
        self.product = ProductFactory(name='Test Product', price=10.0)
        self.cart_item = CartItemFactory(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def get_url(self, uuid):
        return reverse(
            'cart-item-retrieve-update-destroy', 
            kwargs={'uuid': uuid}
        )  

    def test_retrieve_cart_item_authenticated_user(self):
        """Test retrieve cart item for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.get(self.get_url(self.cart_item.uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload']['product'], self.product.uuid)
        self.assertEqual(response.data['payload']['quantity'], 2)
        self.assertEqual(response.data['payload']['cart'], self.cart.uuid)

    def test_retrieve_cart_item_as_guest_user(self):
        """Test retrieve cart item as guest user."""
        response = self.client.get(
            self.get_url(self.cart_item.uuid),
            REMOTE_ADDR='127.0.0.1'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_cart_item_with_other_user(self):
        """Test retrieve cart item for other user permission."""
        user = UserProfileFactory().user
        self.client.force_login(user)
        response = self.client.get(self.get_url(self.cart_item.uuid))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retreive_cart_item_for_guest_user(self):
        """Test retrieve cart item for guest user."""
        cart = CartFactory(ip_address='127.0.0.2', profile=None)
        cart_item =CartItemFactory(
            cart=cart,
            product=self.product,
            quantity=1
        )
        response = self.client.get(self.get_url(cart_item.uuid), REMOTE_ADDR='127.0.0.2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload']['product'], self.product.uuid)
        self.assertEqual(response.data['payload']['quantity'], 1)
        self.assertEqual(response.data['payload']['cart'], cart.uuid)

    def test_update_cart_item_authenticated_user(self):
        """Test update cart item for authenticated user."""
        self.client.force_login(self.profile.user)
        data = {
            'quantity': 3
        }
        response = self.client.put(self.get_url(self.cart_item.uuid), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Cart item updated successfully.')
        self.assertEqual(response.data['payload']['quantity'], 3)

    def test_update_cart_item_authenticated_user_invalid_quantity(self):
        """Test update cart item for authenticated user with invalid quantity."""
        self.client.force_login(self.profile.user)
        data = {
            'quantity': 0
        }
        response = self.client.put(self.get_url(self.cart_item.uuid), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            'quantity: Quantity cannot be less than 1. Try deleting the item instead.'
        )
        self.assertEqual(response.data['status'], 'error')

    def test_update_cart_item_with_unauthenticated_user(self):
        """Test update cart item for other user permission."""
        data = {
            'quantity': 2
        }
        
        response = self.client.put(self.get_url(self.cart_item.uuid), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_cart_item_with_other_user(self):
        """Test update cart item for other user permission."""
        user = UserProfileFactory().user
        data = {
            'quantity': 2
        }
        self.client.force_login(user)
        response = self.client.put(
            self.get_url(self.cart_item.uuid),
            data, REMOTE_ADDR='127.0.0.2'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_cart_item_guest_user(self):
        """Test update cart item for guest user."""
        cart = CartFactory(ip_address='127.0.0.2', profile=None)
        cart_item =CartItemFactory(
            cart=cart,
            product=self.product,
            quantity=1
        )
        data = {
            'quantity': 4
        }
        response = self.client.put(self.get_url(cart_item.uuid), data, REMOTE_ADDR='127.0.0.2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Cart item updated successfully.')
        self.assertEqual(response.data['payload']['quantity'], 4)
        self.assertEqual(response.data['payload']['cart'], cart.uuid)
        self.assertEqual(response.data['payload']['product'], self.product.uuid)

    def test_delete_cart_item_authenticated_user(self):
        """Test delete cart item for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.delete(self.get_url(self.cart_item.uuid))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_cart_item_guest_user(self):
        """Test delete cart item for guest user."""
        cart = CartFactory(ip_address='127.0.0.2', profile=None)
        cart_item =CartItemFactory(
            cart=cart,
            product=self.product,
            quantity=1
        )
        response = self.client.delete(self.get_url(cart_item.uuid), REMOTE_ADDR='127.0.0.2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_cart_item_with_other_user(self):
        """Test delete cart item for other user permission."""
        user = UserProfileFactory().user
        self.client.force_login(user)
        response = self.client.delete(self.get_url(self.cart_item.uuid))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_cart_item_with_unauthenticated_user(self):
        """Test delete cart item for other user permission."""
        response = self.client.delete(self.get_url(self.cart_item.uuid), REMOTE_ADDR='127.0.0.2')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_cart_item_cart_invalid_ip_item(self):
        cart = CartFactory(ip_address='127.0.0.2', profile=None)
        cart_item =CartItemFactory(
            cart=cart,
            product=self.product,
            quantity=1
        )
        response = self.client.delete(self.get_url(cart_item.uuid), REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CartTotalView(APITestCase):
    """Test the CartTotalView view."""
    def setUp(self):
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.cart = CartFactory(
            profile=self.profile,
            ip_address='127.0.0.1',
        )
        self.p1 = ProductFactory(name='Test Product', price=20.0)
        self.p2 = ProductFactory(name='Test Product', price=30.0)
        self.p3 = ProductFactory(name='Test Product', price=70.0)

        self.discountedPrice = (
            self.p1.discounted_price*1 + self.p2.discounted_price*2 + self.p3.discounted_price*3
        )
        self.deliveryFee = Decimal(99.0)

        CartItemFactory(cart=self.cart, product=self.p1, quantity=1)
        CartItemFactory(cart=self.cart, product=self.p2, quantity=2)
        CartItemFactory(cart=self.cart, product=self.p3, quantity=3)

        self.url = reverse('cart-total')

    def test_get_cart_total_authenticated_user(self):
        """Test get cart total for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload']['sub_total'], self.discountedPrice)
        self.assertEqual(response.data['payload']['delivery_fee'], self.deliveryFee)
        self.assertEqual(response.data['payload']['total'], self.discountedPrice+self.deliveryFee)

    def test_get_cart_total_guest_user(self):
        """Test get cart total for guest user."""
        self.cart.profile = None
        self.cart.save()
        response = self.client.get(self.url, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload']['sub_total'], self.discountedPrice)
        self.assertEqual(response.data['payload']['delivery_fee'], self.deliveryFee)
        self.assertEqual(response.data['payload']['total'], self.discountedPrice+self.deliveryFee)


class AddressListCreateAPIViewTests(APITestCase):
    """Test the AddressListCreateAPIView view."""
    def setUp(self):
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.url = reverse('address-list-create')
        self.address1 = AddressFactory(
            profile=self.profile,
            address_line='123 Main St',
            near_by='Near Park',
            city='Test City',
            state='Test State',
            country='India',
            pincode='110001',
        )
        self.address2 = AddressFactory(
            profile=self.profile,
            address_line='456 Elm St',
            near_by='Near School',
            city='Another City',
            state='Another State',
            country='India',
            pincode='110002',
        )

    def test_get_addresses_authenticated_user(self):
        """Test get addresses for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']['addresses']), 2)

    def test_get_addresses_guest_user(self):
        """Test get addresses for guest user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_address_authenticated_user(self):
        """Test create address for authenticated user."""
        self.client.force_login(self.profile.user)
        data = {
            'address_line': '123 Main St',
            'near_by': 'Near Park',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'India',
            'pincode': '110001',
            'type': AddressChoices.OFFICE,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Address created successfully.')
        self.assertEqual(response.data['payload']['address_line'], data['address_line'])
        self.assertEqual(response.data['payload']['type'], AddressChoices.OFFICE)

    def test_create_address_guest_user(self):
        """Test create address for guest user."""
        data = {
            'address_line': '123 Main St',
            'near_by': 'Near Park',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'India',
            'pincode': '110001',
            'type': AddressChoices.OFFICE,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AddressRetrieveUpdateDestroyAPIViewTests(APITestCase):
    """Test the AddressRetrieveUpdateDestroyAPIView view."""
    def setUp(self):
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.address = AddressFactory(profile=self.profile)
        self.url = reverse('address-retrieve-update-destroy',
                           kwargs={'uuid': self.address.uuid})

    def test_retrieve_address_authenticated_user(self):
        """Test retrieve address for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['payload']['address_line'],
            self.address.address_line)

    def test_retrieve_address_guest_user(self):
        """Test retrieve address for guest user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_address_authenticated_user(self):
        """Test update address for authenticated user."""
        self.client.force_login(self.profile.user)
        data = {
            'address_line': '789 New St',
            'near_by': 'Near Mall',
            'city': 'Updated City',
            'state': 'Updated State',
            'country': 'India',
            'pincode': '110003',
            'type': AddressChoices.HOME,
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Address updated successfully.')
        self.assertEqual(response.data['payload']['address_line'], data['address_line'])
    
    def test_update_address_guest_user(self):
        """Test update address for guest user."""
        data = {
            'address_line': '789 New St',
            'near_by': 'Near Mall',
            'city': 'Updated City',
            'state': 'Updated State',
            'country': 'India',
            'pincode': '110003',
            'type': AddressChoices.HOME,
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_address_authenticated_user(self):
        """Test delete address for authenticated user."""
        self.client.force_login(self.profile.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            response.data['message'], 'Address deleted successfully.'
        )

    def test_delete_address_guest_user(self):
        """Test delete address for guest user."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
