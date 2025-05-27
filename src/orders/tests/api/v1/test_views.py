import json
import uuid

from unittest.mock import patch

from django.test import Client, TestCase

from orders.constants import SHIPPING_CHARGE
from orders.choices import OrderStatusChoices, PaymentMethodChoices

from products.factories import ProductFactory

from users.factories import (
    AddressFactory, CartFactory,
    CartItemFactory, UserProfileFactory
)


class CreateOrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = UserProfileFactory()
        self.product1 = ProductFactory(name='Product 1', price=100, discount_in_percent=0)
        self.product2 = ProductFactory(name='Product 2', price=200, discount_in_percent=0)
        self.cart = CartFactory(profile=self.profile)
        self.cart_item1 = CartItemFactory(
            product=self.product1, quantity=2, cart=self.cart,
        )
        self.cart_item2 = CartItemFactory(
            product=self.product2, quantity=1, cart=self.cart,
        )
        self.address = AddressFactory(
            profile=self.profile, address_line='123 Main St',
            city='Test City', state='Test State', pincode='123456'
        )

        self.razorpay_success_response = {
            "id": "order_EKwxwAgItmmXdp",
            "entity": "order",
            "amount": 40000,
            "amount_paid": 0,
            "amount_due": 40000,
            "currency": "INR",
            "receipt": "receipt#1",
            "offer_id": None,
            "status": "created",
            "attempts": 0,
            "notes": [],
            "created_at": 1582628071
        }

        self.razorpay_bad_response = {
            "error": {
                "code": "BAD_REQUEST_ERROR",
                "description": "The amount must be atleast INR 1.00",
                "source": "business",
                "step": "payment_initiation",
                "reason": "input_validation_failed",
                "metadata": {},
                "field": "amount"
            }
        }

        self.url = '/api/v1/orders/create-order/'

    @patch('orders.handlers.create_order.razorpay_client.create_order')
    def test_create_order_view(self, razorpay_create_order):
        """Test the create order view with a successful Razorpay response."""
        razorpay_create_order.return_value = self.razorpay_success_response

        self.client.force_login(self.profile.user)

        response = self.client.post(self.url, json.dumps({
            'address_id': str(self.address.uuid),
            'payment_method': PaymentMethodChoices.RAZORPAY,
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('order_id', response_data['payload'])
        self.assertEqual(49900, response_data['payload']['payable_amount'])
        self.assertEqual(response_data['payload']['payment_method'],
                         PaymentMethodChoices.RAZORPAY)

        order_id = response_data['payload']['order_id']
        order = self.profile.orders.get(uuid=order_id)
        self.assertEqual(order.status, OrderStatusChoices.PLACED)
        self.assertEqual(order.shipping_address, self.address)
        self.assertEqual(order.profile, self.profile)
        self.assertEqual(order.products_in_order.count(), 2)
        self.assertEqual(order.order_amount, 400)
        self.assertEqual(order.total_amount, 400+SHIPPING_CHARGE)
        self.assertEqual(order.payment_method, PaymentMethodChoices.RAZORPAY)

    @patch('orders.handlers.create_order.razorpay_client.create_order')
    def test_create_order_with_new_address(self, razorpay_create_order):
        """Test the create order view with a new address and a successful Razorpay response."""
        razorpay_create_order.return_value = self.razorpay_success_response
        self.client.force_login(self.profile.user)
        
        response = self.client.post(self.url, data=json.dumps({
            "address_data": {
                "address_line": "456 Another St",
                "city": "Another City",
                "state": "Another State",
                "pincode": "654321"
            },
            "payment_method": PaymentMethodChoices.RAZORPAY,
        }),
        content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        order_id = response.json()['payload']['order_id']
        order = self.profile.orders.get(uuid=order_id)
        shipping_address = order.shipping_address
        self.assertEqual(shipping_address.address_line, "456 Another St")
        self.assertEqual(shipping_address.city, "Another City")
        self.assertEqual(shipping_address.state, "Another State")
        self.assertEqual(shipping_address.pincode, "654321")

    @patch('orders.handlers.create_order.razorpay_client.create_order')
    def test_create_order_duplicate_email_inactive_user(self, razorpay_create_order):
        """Test the create order view with a duplicate email and an inactive user."""
        razorpay_create_order.return_value = self.razorpay_success_response
        self.profile.user.is_active = False
        self.profile.user.save()
        
        response = self.client.post(self.url, data=json.dumps({
            "address_id": str(self.address.uuid),
            "user_data": {
                "email": self.profile.user.email,
                "first_name": "Test",
                "last_name": "User",
                "mobile_number": "1234567890"
            },
            "payment_method": PaymentMethodChoices.RAZORPAY
        }),
        content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
    
    @patch('orders.handlers.create_order.razorpay_client.create_order')
    def test_create_order_duplicate_email_inactive_user_new_address(self, razorpay_create_order):
        """Test the create order view with a new address and a duplicate email."""
        razorpay_create_order.return_value = self.razorpay_success_response
        self.profile.user.is_active = False
        self.profile.user.save()
        
        response = self.client.post(self.url, data=json.dumps({
            "address_data": {
                "address_line": "456 Another St",
                "city": "Another City",
                "state": "Another State",
                "pincode": "654321"
            },
            "user_data": {
                "email": self.profile.user.email,
                "first_name": "Test",
                "last_name": "User",
                "mobile_number": "1234567890"
            },
            "payment_method": PaymentMethodChoices.RAZORPAY
        }),
        content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        order_id = response.json()['payload']['order_id']
        shipping_address = self.profile.orders.get(uuid=order_id).shipping_address
        self.assertEqual(shipping_address.address_line, "456 Another St")
        self.assertEqual(shipping_address.city, "Another City")
        self.assertEqual(shipping_address.state, "Another State")
        self.assertEqual(shipping_address.pincode, "654321")
        

    def test_create_order_view_invalid_address_id(self):
        """Test the create order view with a successful Razorpay response."""
        user2 = UserProfileFactory().user

        self.client.force_login(user2)

        response = self.client.post(self.url, {
            'address_id': uuid.uuid4(),  # Invalid address id
        })

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "Invalid address id."
        )

    def test_create_order_view_no_address(self):
        """Test the create order view no address provided."""
        user2 = UserProfileFactory().user

        self.client.force_login(user2)

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "Either address_id or address_data must be provided."
        )

    def test_create_order_view_no_cart(self):
        """Test the create order view no cart."""

        self.client.force_login(self.profile.user)
        self.cart.delete()

        response = self.client.post(self.url, {
            'address_id': self.address.uuid,
        })

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "No cart found for the user."
        )

    def test_create_order_view_no_cart_item(self):
        """Test the create order view no cart items."""

        self.client.force_login(self.profile.user)
        self.cart.cart_items.all().delete()

        response = self.client.post(self.url, json.dumps({
            'address_id': str(self.address.uuid),
            "payment_method": PaymentMethodChoices.RAZORPAY
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "Cart is empty. Cannot create order."
        )

    def test_create_order_as_anonymous_user(self):
        """Test the create order view as an anonymous user."""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)

    def test_create_order_duplicate_email(self):
        """Test the create order view with duplicate email."""
        response = self.client.post(self.url, data = json.dumps({
            'user_data': {
                'email': self.profile.user.email,
                'first_name': 'Test',
                'last_name': 'User',
                'mobile_number': '1234567890'
            }
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "email: user with this email address already exists."
        )

    def test_create_order_duplicate_mobile_number(self):
        """Test the create order view with duplicate mobile number."""
        response = self.client.post(self.url, data = json.dumps({
            'user_data': {
                'email': 'test@mail.com',
                'first_name': 'Test',
                'last_name': 'User',
                'mobile_number': self.profile.user.mobile_number
            }
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(
            response_data['message'],
            "mobile_number: user with this mobile number already exists."
        )

    def test_create_order_COD(self):
        """Test the create order view with a successful COD."""

        self.client.force_login(self.profile.user)

        response = self.client.post(self.url, json.dumps({
            'address_id': str(self.address.uuid),
            'payment_method': PaymentMethodChoices.COD,
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('order_id', response_data['payload'])
        self.assertEqual(49900, response_data['payload']['payable_amount'])
        self.assertEqual(response_data['payload']['payment_method'], PaymentMethodChoices.COD)

        order_id = response_data['payload']['order_id']
        order = self.profile.orders.get(uuid=order_id)
        self.assertEqual(order.status, OrderStatusChoices.PLACED)
        self.assertEqual(order.shipping_address, self.address)
        self.assertEqual(order.profile, self.profile)
        self.assertEqual(order.products_in_order.count(), 2)
        self.assertEqual(order.order_amount, 400)
        self.assertEqual(order.total_amount, 400+SHIPPING_CHARGE)
        self.assertEqual(order.payment_method, PaymentMethodChoices.COD)
