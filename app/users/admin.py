from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.


class UserAdminConfig(UserAdmin):
    model = models.User
    search_fields = ('phone_number','full_name')
    list_filter = ('email', 'phone_number', 'is_active',)
    ordering = ('id',)
    list_display = ('__str__', 'email',  'is_active', 'verified', 'phone_number')
    fieldsets = (
        (None, {'fields': (
            'full_name',
            'email',
            'phone_number',
            'profile_picture',
            'password',
            )}),
        ('Permissions',
         {
             'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'verified',
                'groups',
                'user_permissions'
             )
         }),
    )

    # fieldsets to add a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'full_name',
                'email',
                'phone_number',
                'profile_picture',
                'password1',
                'is_active',
                'password2',
                'is_staff',
                'groups',
                'user_permissions'
                )}
         ),
    )


admin.site.register(models.User, UserAdminConfig)
