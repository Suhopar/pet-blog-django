from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """

    Customization of displaying information about a user in the administrative panel.
    Adding the ability to change the role(admin/user).

    """
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'usual_ban', 'absolute_ban')
    list_filter = ('is_staff', 'username', 'email', 'role', 'usual_ban', 'absolute_ban')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_about', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
        ('Banning', {'fields': ('usual_ban', 'absolute_ban')}),
    )

    def role(self, obj):
        return obj.role

    role.admin_order_field = 'role'
    role.short_description = 'Role'

admin.site.register(CustomUser, CustomUserAdmin)
