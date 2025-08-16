from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from server.apps.management.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
