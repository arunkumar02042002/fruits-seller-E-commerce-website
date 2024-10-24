from django.urls import path

from .views import TestimonialAddView

urlpatterns = [
    path("testimonials/add/", view=TestimonialAddView.as_view(), name="testimonial-add")
]
