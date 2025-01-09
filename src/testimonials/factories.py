from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory

from testimonials.models import Testimonial
from testimonials.choices import TestimonialRatingChoices, TestimonialStatusChoices

User = get_user_model()

class TestimonialFactory(DjangoModelFactory):
    """Factory for creating Testimonial instances."""

    class Meta:
        """Meta class."""

        model = Testimonial

    name = factory.Faker('name')
    email = factory.Faker('email')
    profession = factory.Faker('job')
    feedback = factory.Faker('text', max_nb_chars=200)

