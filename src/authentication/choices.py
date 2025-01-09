from django.utils.translation import gettext_lazy as _
from django.db import models

class UserRoleChoices(models.TextChoices):
    """Choices to differentiate users."""
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")
    CUSTOMER_CARE = "CUSTOMER_CARE", _("Customer Care")
