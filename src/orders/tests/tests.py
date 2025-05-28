from django.test import TestCase

# Create your tests here.
class OrderSuccessViewTestCase(TestCase):
    """Test case for OrderSuccessView."""
    
    def setUp(self):
        """Set up the test case."""
        self.client = self.client_class()
    
    def test_order_success_view(self):
        """Test the order success view."""
        response = self.client.get('/orders/success/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')


class OrderFailureViewTestCase(TestCase):
    """Test case for OrderFailureView."""
    
    def setUp(self):
        """Set up the test case."""
        self.client = self.client_class()
    
    def test_order_failure_view(self):
        """Test the order failure view."""
        response = self.client.get('/orders/failed/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_failed.html')
