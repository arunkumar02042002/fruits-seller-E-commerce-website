from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .choices import ContactUsStatusChoice, TestimonialRatingChoices

User = get_user_model()


# Create your models here.
class ContactUs(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="queries",
    )
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email address"), db_index=True)
    query = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=ContactUsStatusChoice.choices,
        default=ContactUsStatusChoice.PENDING,
    )

    assigned_to = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}_{self.email}"


class Testimonial(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )
    name = models.CharField(_("name"), max_length=255, db_index=True)
    email = models.EmailField(_("email address"), db_index=True, null=True, blank=True)
    profession = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.CharField(
        max_length=1, choices=TestimonialRatingChoices.choices, db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}_{self.email}"
