from django.contrib.auth import get_user_model
from django.test import TestCase

from contact.choices import ContactUsStatusChoice
from contact.factories import ContactUsFactory

from users.factories import UserFactory

User = get_user_model()


class ContactUsModelTests(TestCase):

    def setUp(self):
        """Set up users for testing the model."""
        self.user = UserFactory(
            email="test_user@email.com"
        )
        self.assigned_user = UserFactory(
            email="test@email.com"
        )

    def test_create_contact_us_instance(self):
        """Test creating a ContactUs instance."""
        contact = ContactUsFactory(
            created_by=self.user,
            name="John Doe",
            email="john.doe@example.com",
            query="This is a test query.",
            assigned_to=self.assigned_user,
        )
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.query, "This is a test query.")
        self.assertEqual(contact.created_by, self.user)
        self.assertEqual(contact.assigned_to, self.assigned_user)

    def test_default_status_value(self):
        """Test the default status value is PENDING."""
        contact = ContactUsFactory(
            created_by=self.user,
            name="John Doe",
            email="john.doe@example.com",
            query="This is a test query.",
        )
        self.assertEqual(contact.status, ContactUsStatusChoice.NOT_SET)

    def test_contact_us_with_null_user_and_assigned_to(self):
        """Test that user and assigned_to can be null."""
        contact = ContactUsFactory(
            name="Jane Doe", email="jane.doe@example.com", query="Another test query."
        )
        self.assertIsNone(contact.created_by)
        self.assertIsNone(contact.assigned_to)

    def test_created_by_not_assigned_to(self):
        """Test that created_by is not same as assigned_to constraint."""
        creator = UserFactory()
        contact = ContactUsFactory(
            name="Jane Doe", email="jane.doe@example.com", query="Another test query."
        )

        with self.assertRaises(Exception) as context:
            contact.created_by = creator
            contact.assigned_to = creator
            contact.save()

        self.assertEqual(
            "CHECK constraint failed: created_by_not_assigned_to", str(context.exception)
        )
