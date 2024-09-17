from django.contrib import admin
from .models import ContactUs


# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("email", "user__username", "name")
    ordering = ("-created_at",)


admin.site.register(ContactUs, ContactUsAdmin)
