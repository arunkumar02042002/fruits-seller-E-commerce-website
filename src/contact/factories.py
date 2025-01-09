from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from contact.choices import ContactUsStatusChoice
from contact.models import ContactUs



class ContactUsFactory(DjangoModelFactory):
    """Factory to create ContactUs instances."""

    class Meta:
        """Meta class."""

        model = ContactUs

    name = Faker("name")
    email = Faker("email")
    query = Faker("paragraph")
