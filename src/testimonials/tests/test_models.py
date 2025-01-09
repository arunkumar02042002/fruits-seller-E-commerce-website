from django.db import IntegrityError
from django.test import TestCase

from testimonials.choices import (
    TestimonialRatingChoices,
    TestimonialStatusChoices
)
from testimonials.factories import TestimonialFactory

from users.factories import UserFactory

class TestimonialModelTests(TestCase):

    def setUp(self):
        """Set up any necessary data for the tests."""
        self.user = UserFactory(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_create_testimonial(self):
        """Test creating a testimonial with valid data."""
        testimonial = TestimonialFactory(
            created_by=self.user,
            name="John Doe",
            email="john.doe@example.com",
            profession="Software Engineer",
            feedback="Great service!",
        )
        self.assertEqual(testimonial.name, "John Doe")
        self.assertEqual(testimonial.email, "john.doe@example.com")
        self.assertEqual(testimonial.rating, TestimonialRatingChoices.FIVE)
        self.assertEqual(testimonial.status, TestimonialStatusChoices.NOT_SET)

    def test_update_testimonial(self):
        """Test updating a testimonial's feedback and rating."""
        testimonial = TestimonialFactory(
            created_by=self.user,
            name="Sam Williams",
            email="sam.williams@example.com",
            profession="HR Manager",
            feedback="Good service overall.",
            rating=TestimonialRatingChoices.FOUR,
        )
        # Update the testimonial
        testimonial.feedback = "Excellent service!"
        testimonial.rating = TestimonialRatingChoices.FIVE
        testimonial.save()

        testimonial.refresh_from_db()
        self.assertEqual(testimonial.feedback, "Excellent service!")
        self.assertEqual(testimonial.rating, TestimonialRatingChoices.FIVE)

    def test_approved_by_cannot_be_none_for_approved_testimonials(self):
        """Test approved_by_cannot_be_none_for_approved_testimonials."""
        with self.assertRaises(IntegrityError):
            TestimonialFactory(
            is_approved=True
        )
