from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

from users.choices import AddressChoices

User = get_user_model()


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photos", blank=True, null=True
    )
    mobile = models.CharField(
        max_length=10, blank=True,
        null=True, unique=True,
        db_index=True, verbose_name='Mobile Number'
    )
    alternate_number = models.CharField(
        max_length=10, blank=True, null=True,
        unique=True, db_index=True,
        verbose_name='Alternate Number',
    )

    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}, {self.pin_code}"

    def __str__(self):
        return f"{self.user.email}_{self.user.role}"

class Address(BaseModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    address_line = models.CharField(max_length=250, blank=True, null=True)
    near_by = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)

    type = models.CharField(
        max_length=20, choices=AddressChoices, 
        default=AddressChoices.HOME
    )

    # To locate user
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)

    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}, {self.pin_code}"
