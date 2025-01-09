from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.choices import UserRoleChoices

from common.models import BaseModel

from contact.choices import ContactUsStatusChoice


User = get_user_model()

# Create your models here.
class ContactUs(BaseModel):
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email address"), db_index=True)
    query = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=ContactUsStatusChoice.choices,
        default=ContactUsStatusChoice.NOT_SET,
    )

    assigned_to = models.ForeignKey(
        to=User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='queries_assigned'
    )

    class Meta:
        """Meta for Contact Us"""
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

        constraints = [
            models.CheckConstraint(
                check=~models.Q(created_by=models.F("assigned_to")),
                name="created_by_not_assigned_to",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}_{self.email}"
