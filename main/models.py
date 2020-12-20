from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.


def user_deleted():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Project(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = ('in_progress', _('IN PROGRESS'))
        STOPPED = ('stopped', _('STOPPED'))
        FINISH = ('finish', _('FINISH'))

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
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS)
    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class Ticket(models.Model):
    class Priority(models.TextChoices):
        GREEN = ('low', _('LOW'))
        YELLOW = ('medium', _('MEDIUM'))
        RED = ('high', _('HIGH'))

    class Status(models.TextChoices):
        WAITING = ('waiting', _('WAITING FOR ASSIGNMENT'))
        ASSIGNED = ('assigned', _('ASSIGNED'))
        CLOSED = ('closed', _('CLOSED'))

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Project")
    )

    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_submitter_of",
        verbose_name=_("Submitter")
    )

    priority = models.CharField(
        _(Priority),
        choices=Priority.choices,
        max_length=20
    )

    status = models.CharField(
        _(Status),
        choices=Status.choices,
        max_length=20,
        default=Status.WAITING
    )
    assign_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_assign_to"
    )
    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.project.name}:{self.pk}'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class Comment(models.Model):
    @staticmethod
    def get_image_path(instance, filename):
        return f'comments/{instance.ticket.project.title}/{instance.ticket.id}/filename'

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    attachment = models.ImageField(
        _("Attachment"),
        upload_to=get_image_path
    )
    date_created = models.DateTimeField(
        _("Date Created"),
        auto_now_add=True
    )
    last_edit = models.DateTimeField(
        _("Last Edit"),
        auto_now=True
    )
