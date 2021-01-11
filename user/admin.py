from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_staff',)
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login',)

    list_filter = ()
    # for many to many fields sidebyside form
    filter_horizontal = ('is_manager_in',)
    fieldsets = ()  # for admin page form category purpose


admin.site.register(CustomUser, AccountAdmin)
admin.site.register(Profile)
