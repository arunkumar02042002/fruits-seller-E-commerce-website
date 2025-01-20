from django.contrib import admin

from testimonials.models import Testimonial

# Register your models here.
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for Testimonial Model."""
    list_display = ("name", "email", "profession", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("name", "email", "profession")
    ordering = ("-created_at",)

admin.site.register(Testimonial, TestimonialAdmin)