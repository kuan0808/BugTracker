from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from PIL import Image


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('Email Address'), unique=True)
    username = models.CharField(_('Username'), max_length=20, unique=True)
    first_name = models.CharField(_('First Name'), max_length=20)
    last_name = models.CharField(_('Last Name'), max_length=20)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('Last Login'), auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('user.views.ProfileView', args=[str(self.username)])

    def get_full_name(self):
        """
        # Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "    Returns the short name for the user."
        return self.username

    def nature_key(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('The user')
        verbose_name_plural = _('Users')


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image.name == 'default.jpg':
            return

        def make_square(im, fill_color=(0, 0, 0, 0)):
            x, y = im.size
            size = min(x, y)
            if x != y:
                new_im = Image.new('RGBA', (size, size), fill_color)
                new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
                return new_im
            return im
        img = Image.open(self.image.path)
        img = make_square(img)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            print(self.image.name)
            try:
                img.save(self.image.path)
            except:
                img = img.convert("RGB")
                img.save(self.image.path)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('User Profiles')
