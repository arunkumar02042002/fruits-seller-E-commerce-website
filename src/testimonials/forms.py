from django import forms

from testimonials.models import Testimonial


class TestimonialCreateForm(forms.ModelForm):
    """Form for Testimonial Creation"""

    class Meta:
        """Meta class."""

        model = Testimonial
        fields = ("name", "email", "profession", "feedback", "rating")

        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 5, "cols": 10}),
        }
