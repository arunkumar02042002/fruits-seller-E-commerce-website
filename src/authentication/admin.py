from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "phone", "name", "type", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "name",
                    "type",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
