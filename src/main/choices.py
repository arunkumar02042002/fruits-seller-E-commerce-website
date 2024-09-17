from django.db import models


class ContactUsStatusChoice(models.TextChoices):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class TestimonialRatingChoices:
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"

    choices = [
        (ONE, "One"),
        (TWO, "Two"),
        (THREE, "Three"),
        (FOUR, "Four"),
        (FIVE, "Five"),
    ]
