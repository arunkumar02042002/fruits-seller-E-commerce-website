from django.urls import path

from testimonials.views import TestimonialAddView

urlpatterns = [
    path(
        "testimonials/<uuid>/<uidb64>/<token>/",
        view=TestimonialAddView.as_view(),
        name="add_testimonial",
    ),
]
