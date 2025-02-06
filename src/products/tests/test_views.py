import uuid

from django.test import TestCase
from django.urls import reverse

from products.factories import ProductFactory

class TestShopDetailView(TestCase):
    """Test ShopDetailView."""
    def setUp(self):
        self.product = ProductFactory()
        for _ in range(5):
            ProductFactory(category=self.product.category)
        self.url = reverse('shop-detail', kwargs={'uuid': self.product.uuid})

    def test_html_template_rendered(self):
        """Test html templated used in ShopDetailView."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'products/shop_details.html')

    def test_context_data(self):
        """Test context data in ShopDetailView."""
        response = self.client.get(self.url)
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(len(response.context['related_products']), 5)

    def test_product_not_exists(self):
        """Test 404 response in ShopDetailView."""
        response = self.client.get(reverse('shop-detail', kwargs={'uuid': uuid.uuid4()}))
        self.assertEqual(response.status_code, 404)
