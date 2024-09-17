from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .choices import ContactUsStatusChoice

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
