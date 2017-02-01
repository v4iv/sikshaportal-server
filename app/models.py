from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.utils import timezone
from django.utils.http import urlquote


class SikshaUserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        now = timezone.now()

        if not email:
            raise ValueError('Email is Required!')

        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        return self._create_user(first_name, last_name, email, password, False, False, **extra_fields)

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        return self._create_user(first_name, last_name, email, password, True, True, **extra_fields)


class SikshaUser(AbstractBaseUser, PermissionsMixin):
    """
    A Custom User model with admin-compliant Permissions.

    First Name, Last Name and Email are required.
    """
    email = models.EmailField(_('Email Address'), max_length=254, unique=True)
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=30)
    is_staff = models.BooleanField(_('Staff Status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text='Designates whether this user should be treated as'
                                              'active. Unselect this instead of deleting accounts')
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    objects = SikshaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Full Name.
        :return: Returns the first_name plus the last_name, with space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Short Name.
        :return: Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        :param subject: Subject of the mail.
        :param message:  Message content of the mail.
        :param from_email: the senders email.
        """
        send_mail(subject, message, from_email, [self.email])


class SikshaUserProfile(models.Model):
    user = models.OneToOneField(SikshaUser, on_delete=models.CASCADE, to_field='email', unique=True)
    display_picture = models.ImageField(upload_to="uploads/displaypictures", default="uploads/displaypictures/male-silhouette.jpg")
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    SEX_CHOICES = (
        (UNKNOWN, 'Do Not Wish To Disclose'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES, default=UNKNOWN)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            SikshaUserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=SikshaUser)

    def create(self):
        self.save()

    def __str__(self):
        return self.user.get_full_name()
