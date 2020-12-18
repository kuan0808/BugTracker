from django.db import models
from django.utils.translation import ugettext_lazy as _
from user.models import CustomUser
# Create your models here.


class Project(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Descriptions'), max_length=500)
    manager = models.ManyToManyField(
        CustomUser, verbose_name=_("Manager"), related_name="is_manager_in")
    member = models.ManyToManyField(
        CustomUser, verbose_name=_("Member"), related_name="is_member_in")


class Ticket(models.Model):
    pass
