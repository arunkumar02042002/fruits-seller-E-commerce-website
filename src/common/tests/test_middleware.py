from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from common.utils import GlobalVariable

from users.factories import UserFactory

class TestLogMiddleware(TestCase):
    """Test for LogMiddleware."""

    def setUp(self):
        """Prepare Data."""
        self.url = reverse('products')
        self.user = UserFactory()
        self.client = APIClient()

        return super().setUp()
    
    def test_process_request(self):
        """Test user_id is correctly set."""

        self.client.get(self.url)
        self.assertEqual(GlobalVariable().get_val('user_id'), None)

        self.client.force_login(self.user)
        self.client.get(self.url) # Authenticated request

        self.assertEqual(GlobalVariable().get_val('user_id'), self.user.uuid)

