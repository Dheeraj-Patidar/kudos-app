from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Kudos, Organization, User


class CustomUserAdmin(UserAdmin):
    list_display = ["email", "organization", "is_staff", "kudos_count", "kudos_last_reset"]
    ordering = ["email"]
    search_fields = ("email", "organization")
    list_filter = ("is_staff", "is_superuser", "is_active")
    readonly_fields = ("kudos_count","kudos_last_reset", "date_joined")
    # Customize the fieldsets to remove 'username'
    fieldsets = (
        (None, {"fields": ("email", "password", "organization")}),
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
        ("personal", {"fields": ("first_name", "last_name")}),
        ("Kudos", {"fields": ("kudos_count", "kudos_last_reset")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Define fields for user creation in the admin panel
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "organization",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)


admin.site.register(Organization, OrganizationAdmin)


class KudosAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "message", "timestamp"]
    search_fields = ("sender", "receiver")
    list_filter = ("timestamp",)
    readonly_fields = ("timestamp",)

    fieldsets = (
        
        ("kudos details", {"fields": ("sender", "sender_first_name", "sender_last_name", "receiver", "message")}),
        ("Important dates", {"fields": ("timestamp",)}),
    )


admin.site.register(Kudos, KudosAdmin)
