from django.test import TestCase
from django.urls import reverse


class AboutUsViewTests(TestCase):
    """Test about us view."""
    def test_about_us_template_used_and_status_code(self):
        """Test that the AboutUsView uses the correct template and status code."""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/about.html")


class HomeViewTests(TestCase):
    """Test about us view."""
    def test_home_template_used_and_status_code(self):
        """Test that the HomeView uses the correct template and status code."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")