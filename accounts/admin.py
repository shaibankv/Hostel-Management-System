from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserList


class CustomUserAdmin(UserAdmin):
    model = UserList

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )


admin.site.register(UserList, CustomUserAdmin)