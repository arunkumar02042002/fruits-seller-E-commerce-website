from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from contact.choices import ContactUsStatusChoice
from contact.forms import ContactUsForm
from contact.models import ContactUs

from users.factories import UserFactory

class ContactUsViewTests(TestCase):

    def setUp(self):
        """Set up any necessary data for the tests."""
        self.user = UserFactory(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.url = reverse("contact")

    def test_get_contact_us_view(self):
        """Test that the ContactUsView renders the contact form on GET request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/contact.html")
        self.assertIsInstance(response.context["form"], ContactUsForm)

    def test_post_invalid_contact_us_form(self):
        """Test that invalid form submission renders the form with errors."""

        # Submitting an empty form
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/contact.html")
        form = response.context["form"]

        # The form should be invalid
        self.assertFalse(form.is_valid())

    def test_post_valid_contact_us_form(self):
        """Test that a valid form submission saves the query and redirects."""
        valid_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "query": "This is a test query.",
        }

        # Make the POST request with valid form data
        response = self.client.post(self.url, data=valid_data)

        # Check that the query was saved to the database
        contact_us = ContactUs.objects.filter(email="john.doe@example.com").first()
        self.assertIsNotNone(contact_us)
        self.assertEqual(contact_us.name, "John Doe")
        self.assertEqual(contact_us.query, "This is a test query.")
        self.assertEqual(contact_us.status, ContactUsStatusChoice.PENDING)
        self.assertIsNone(contact_us.created_by)
        self.assertIsNone(contact_us.assigned_to)

        # Check that a success message is added to the messages framework
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(
            str(messages[0]),
            "Your query has been submitted. Our representative will contact you shortly.",
        )

        # Check the redirection after form submission
        self.assertRedirects(response, self.url)

    def test_post_form_assigns_user_if_exists(self):
        """Test that the form assigns the correct user based on the email."""
        valid_data = {
            "name": "John Doe",
            # Email that matches the user created in setUp()
            "email": "testuser@example.com",
            "query": "This is a test query.",
        }

        self.client.post(self.url, data=valid_data)
        contact_us = ContactUs.objects.filter(email="testuser@example.com").first()
        self.assertEqual(contact_us.created_by, self.user)