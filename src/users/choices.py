from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressChoices(models.TextChoices):
    """Choices to differentiate Address."""
    HOME = "HOME", _("Home")
    OFFICE = "OFFICE", _("Office")
    OTHER = "OTHER", _("Other")
