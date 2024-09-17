from rest_framework import serializers

from main.models import Testimonial


class TestimonialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ("name", "profession", "email", "feedback", "rating")
