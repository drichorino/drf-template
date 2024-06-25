from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "email",
        "name",
        "user_type",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_created",
        "date_updated",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "user_type"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Information",
            {
                "fields": (
                    "name",
                    "email",
                    "mobile_number",
                    "company",
                    "designation",
                    "notes",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "user_permissions",
                    "groups",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined", "date_created", "date_updated")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "name")
    ordering = ("username",)


admin.site.register(User, CustomUserAdmin)
