"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from images import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_filter = ('account_type',)
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Account type'),
            {
                'fields': (
                    'account_type',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'account_type',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class AccountAdmin(admin.ModelAdmin):
    """Define the admin pages for account types."""

    ordering = ['id']
    list_display = ['title', ]
    fieldsets = (
        (None, {'fields': ('title',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_basic',
                    'is_premium',
                    'is_enterprise',
                    'is_custom',
                )
            }
        ),
        (_('Available actions'), {'fields': (
            'thumb_size1',
            'thumb_size2',
            'link_to_original',
            'link_to_binary',
            )}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.AccountType, AccountAdmin)
