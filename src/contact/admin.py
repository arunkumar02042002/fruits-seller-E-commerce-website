from django.contrib import admin
from contact.models import ContactUs


# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    """Admin for contact us model."""
    list_display = ("name", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("email", "name")
    ordering = ("-created_at",)

admin.site.register(ContactUs, ContactUsAdmin)
