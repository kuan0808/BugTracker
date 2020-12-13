from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email'), unique=True)
    username = models.CharField(_('username'), max_length=20, unique=True)
    first_name = models.CharField(_('first_name'), max_length=20)
    last_name = models.CharField(_('last_name'), max_length=20)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_admin = models.BooleanField(_('is_admin'), default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('user.views.ProfileView', args=[str(self.username)])

    def get_full_name(self):
        """
        #Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "    Returns the short name for the user."
        return self.username

    def nature_key(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}'s Profile"

