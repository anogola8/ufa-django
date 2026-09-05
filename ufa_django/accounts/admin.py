from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('full_name',)
    list_display = ('email', 'full_name', 'role', 'county', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'county')
    search_fields = ('email', 'full_name', 'phone')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone', 'county', 'ward')}),
        ('Role & permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Security', {'fields': ('is_mfa_enabled', 'last_login_ip')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'last_login_ip')
