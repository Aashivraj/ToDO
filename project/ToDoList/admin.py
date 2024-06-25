from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_name', 'email', 'mobile_number', 'team', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'team')
    fieldsets = (
        (None, {'fields': ('user_name', 'email', 'password', 'mobile_number', 'team', 'role', 'photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'password1', 'password2', 'mobile_number', 'team', 'role', 'photo')}
        ),
    )
    search_fields = ('email', 'user_name', 'mobile_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(Todo)
admin.site.register(SystemSettings)
