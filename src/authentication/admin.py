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
        "date_joined",
    )
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "role", "password")}),
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
    ordering = (
        "-date_joined",
        "email",
    )


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
