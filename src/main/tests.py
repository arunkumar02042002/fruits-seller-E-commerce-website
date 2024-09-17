from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import ContactUs, Testimonial
from .choices import ContactUsStatusChoice
from .forms import ContactUsForm

User = get_user_model()


class ContactUsModelTests(TestCase):

    def setUp(self):
        """Set up users for testing the model."""
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.assigned_user = User.objects.create_user(
            username="assigneduser",
            email="assigneduser@example.com",
            password="password123",
        )

    def test_create_contact_us_instance(self):
        """Test creating a ContactUs instance."""
        contact = ContactUs.objects.create(
            user=self.user,
            name="John Doe",
            email="john.doe@example.com",
            query="This is a test query.",
            assigned_to=self.assigned_user,
        )
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.query, "This is a test query.")
        self.assertEqual(contact.user, self.user)
        self.assertEqual(contact.assigned_to, self.assigned_user)

    def test_default_status_value(self):
        """Test the default status value is PENDING."""
        contact = ContactUs.objects.create(
            user=self.user,
            name="John Doe",
            email="john.doe@example.com",
            query="This is a test query.",
        )
        self.assertEqual(contact.status, ContactUsStatusChoice.PENDING)

    def test_contact_us_str_method(self):
        """Test the string representation of the ContactUs model."""
        contact = ContactUs.objects.create(
            user=self.user,
            name="John Doe",
            email="john.doe@example.com",
            query="This is a test query.",
        )
        self.assertEqual(str(contact), "John Doe_john.doe@example.com")

    def test_contact_us_with_null_user_and_assigned_to(self):
        """Test that user and assigned_to can be null."""
        contact = ContactUs.objects.create(
            name="Jane Doe", email="jane.doe@example.com", query="Another test query."
        )
        self.assertIsNone(contact.user)
        self.assertIsNone(contact.assigned_to)


class TestimonialModelTests(TestCase):

    def setUp(self):
        """Set up any necessary data for the tests."""
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

    def test_create_testimonial(self):
        """Test creating a testimonial with valid data."""
        testimonial = Testimonial.objects.create(
            user=self.user,
            name="John Doe",
            email="john.doe@example.com",
            profession="Software Engineer",
            feedback="Great service!",
            rating="5",
        )
        self.assertEqual(Testimonial.objects.count(), 1)
        self.assertEqual(testimonial.name, "John Doe")
        self.assertEqual(testimonial.email, "john.doe@example.com")
        self.assertEqual(testimonial.rating, "5")

    def test_string_representation(self):
        """Test the string representation of the Testimonial model."""
        testimonial = Testimonial.objects.create(
            user=self.user,
            name="John Doe",
            email="john.doe@example.com",
            profession="Software Engineer",
            feedback="Great service!",
            rating="5",
        )
        self.assertEqual(str(testimonial), "John Doe_john.doe@example.com")

    def test_create_testimonial_without_user(self):
        """Test creating a testimonial without a user (null user field)."""
        testimonial = Testimonial.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            profession="Data Scientist",
            feedback="Amazing experience!",
            rating="4",
        )
        self.assertIsNone(testimonial.user)
        self.assertEqual(testimonial.name, "Jane Smith")

    def test_create_testimonial_without_email(self):
        """Test creating a testimonial without an email (blank email field)."""
        testimonial = Testimonial.objects.create(
            user=self.user,
            name="Michael Brown",
            profession="Product Manager",
            feedback="Loved the product!",
            rating="5",
        )
        # The email field should be None
        self.assertIsNone(testimonial.email)
        self.assertEqual(testimonial.name, "Michael Brown")

    def test_update_testimonial(self):
        """Test updating a testimonial's feedback and rating."""
        testimonial = Testimonial.objects.create(
            user=self.user,
            name="Sam Williams",
            email="sam.williams@example.com",
            profession="HR Manager",
            feedback="Good service overall.",
            rating="4",
        )
        # Update the testimonial
        testimonial.feedback = "Excellent service!"
        testimonial.rating = "5"
        testimonial.save()

        updated_testimonial = Testimonial.objects.get(id=testimonial.id)
        self.assertEqual(updated_testimonial.feedback, "Excellent service!")
        self.assertEqual(updated_testimonial.rating, "5")


class AboutUsViewTests(TestCase):
    def test_about_us_template_used_and_status_code(self):
        """Test that the AboutUsView uses the correct template and status code."""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/about.html")


class ContactUsViewTests(TestCase):

    def setUp(self):
        """Set up any necessary data for the tests."""
        self.user = User.objects.create_user(
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
        self.assertIsNone(contact_us.user)
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

        response = self.client.post(self.url, data=valid_data)
        contact_us = ContactUs.objects.filter(email="testuser@example.com").first()
        self.assertEqual(contact_us.user, self.user)
