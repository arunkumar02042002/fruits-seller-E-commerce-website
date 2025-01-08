from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from factory import Faker, LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from users.models import Address, Profile


User = get_user_model()

class UserFactory(DjangoModelFactory):
    """Create User instances."""

    class Meta:
        """Meta Class."""

        model = User

    email = Sequence(lambda n: 'user%d@email.com' % n)
    username = Sequence(lambda n: 'user%d' % n)
    password = make_password('password')
    first_name = Faker('first_name')
    last_name = Faker('last_name')

class UserProfileFactory(DjangoModelFactory):
    """Create User Profile instances."""

    class Meta:
        """Meta class."""

        model = Profile

    user = SubFactory('users.factories.UserFactory')
    mobile = LazyAttribute(lambda p: '{}'.format(
        FuzzyInteger(6000000000, 9999999999).fuzz()))
    alternate_number = LazyAttribute(lambda p: '{}'.format(
        FuzzyInteger(6000000000, 9999999999).fuzz()))


class AddressFactory(DjangoModelFactory):
    """Create Address instances."""

    class Meta:
        """Meta class."""

        model = Address

    address_line = Faker('address_line')
    near_by = Faker('near_by')
    city = Faker('city')
    state = Faker('state')
    country = 'India'
    pincode = LazyAttribute(lambda p: '{}'.format(
        FuzzyInteger(110000, 999999).fuzz()))

    latitude = Faker('latitude')
    longitude = Faker('longitude')