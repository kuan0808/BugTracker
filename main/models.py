from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.


def user_deleted():
    return CustomUser.objects.get_or_create(username="deleted")[0]


class Project(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = ('in_progress', 'IN PROGRESS')
        STOPPED = ('stoppped', 'STOPPED')


    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(
        _('Descriptions'),
        max_length=500)
    manager = models.ManyToManyField(
        get_user_model(), verbose_name=_("Manager"),
        related_name="is_manager_in")
    member = models.ManyToManyField(
        get_user_model(), verbose_name=_("Member"),
        related_name="is_member_in")
    status = models.CharField(_("Status"),
                              choices=)


class Ticket(models.Model):
    class Priority(models.TextChoices):

    class Status(models.TextChoices):
        pass

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Project"))

    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_submitter_of",
        verbose_name=_("Submitter"))

    priority = models.CharField(_(Priority))

    status = models.CharField(_(Status))
    assign_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_assign_to")
    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True)


class Comment(models.Model):
    pass
