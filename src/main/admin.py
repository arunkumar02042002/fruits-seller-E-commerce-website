from django.contrib import admin
from .models import ContactUs, Testimonial


# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("email", "name")
    ordering = ("-created_at",)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "profession", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("name", "email", "profession")
    ordering = ("-created_at",)


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
