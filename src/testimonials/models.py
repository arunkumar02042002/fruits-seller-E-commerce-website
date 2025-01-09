from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

from testimonials.choices import (
    TestimonialRatingChoices,
    TestimonialStatusChoices
)

User = get_user_model()

class Testimonial(BaseModel):
    """Store Testimonial Data."""

    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email address"), db_index=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    feedback = models.TextField()
    rating = models.IntegerField(
        choices=TestimonialRatingChoices.choices,
        default=TestimonialRatingChoices.FIVE,
        db_index=True,
    )
    status = models.CharField(
        max_length=15,
        choices=TestimonialStatusChoices,
        default=TestimonialStatusChoices.NOT_SET,
    )

    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="testimonials_approved"
    )

    class Meta:
        """Meta for Testimonials."""

        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(is_approved=False) |
                    models.Q(approved_by__isnull=False)
                ),
                name="approved_by_cannot_be_none_for_approved_testimonials"
            ),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name}_{self.email}"
