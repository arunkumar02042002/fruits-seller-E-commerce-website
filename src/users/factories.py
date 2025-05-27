from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from factory import Faker, LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from users.models import Address, Cart, CartItem, Profile


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
    mobile_number = LazyAttribute(lambda o: '{}'.format(
        FuzzyInteger(6000000000, 9999999999).fuzz()))


class UserProfileFactory(DjangoModelFactory):
    """Create User Profile instances."""

    class Meta:
        """Meta class."""

        model = Profile

    user = SubFactory('users.factories.UserFactory')
    alternate_number = LazyAttribute(lambda p: '{}'.format(
        FuzzyInteger(6000000000, 9999999999).fuzz()))


class AddressFactory(DjangoModelFactory):
    """Create Address instances."""

    class Meta:
        """Meta class."""

        model = Address
    
    profile = SubFactory('users.factories.UserProfileFactory')


class CartFactory(DjangoModelFactory):
    """Create Cart instances."""

    class Meta:
        """Meta class."""

        model = Cart

    profile = SubFactory('users.factories.UserProfileFactory')


class CartItemFactory(DjangoModelFactory):
    """Create CartItem instances."""

    class Meta:
        """Meta class."""

        model = CartItem

    cart = SubFactory('users.factories.CartFactory')
    product = SubFactory('products.factories.ProductFactory')
    quantity = FuzzyInteger(1, 10)
