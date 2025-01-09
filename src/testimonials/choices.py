from django.db import models


class TestimonialRatingChoices(models.IntegerChoices):
    """Choices for ratings."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class TestimonialStatusChoices(models.TextChoices):
    """Choices for status."""
    NOT_SET = "NOT_SET"
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
