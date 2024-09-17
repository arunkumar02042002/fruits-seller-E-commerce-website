from django.db import models


class ContactUsStatusChoice(models.TextChoices):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
