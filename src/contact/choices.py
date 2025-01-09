from django.db import models

class ContactUsStatusChoice(models.TextChoices):
    """Choices for ContactUs model."""
    NOT_SET = "NOT_SET"
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"