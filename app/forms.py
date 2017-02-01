from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from app.models import SikshaUser


class SikshaUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kwargs):
        super(SikshaUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SikshaUser
        fields = ("email", "first_name", "last_name",)


class SikshaUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kwargs):
        super(SikshaUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SikshaUser
        fields = ("email", "first_name", "last_name")
