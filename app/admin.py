from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from app.forms import SikshaUserChangeForm, SikshaUserCreationForm
from app.models import SikshaUser


class SikshaUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field

    form = SikshaUserChangeForm
    add_form = SikshaUserCreationForm
    fieldsets = ((_('User'), {'fields': ('email', 'password')}),
                 (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
                 (_('Permissions'),
                  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                 (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
                 )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(SikshaUser, SikshaUserAdmin)
