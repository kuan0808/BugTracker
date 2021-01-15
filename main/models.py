from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


def user_deleted():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Project(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = ('in_progress', _('IN PROGRESS'))
        STOPPED = ('stopped', _('STOPPED'))
        FINISH = ('finish', _('FINISH'))

    title = models.CharField(
        _('Title'),
        max_length=50,
    )
    description = models.TextField(
        _('Descriptions'),
        max_length=500
    )
    manager = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('Manager'),
        related_name="is_manager_in",
        default=None,
        blank=True,
    )
    member = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('Member'),
        related_name="is_member_in",
        default=None,
        blank=True,
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    liked = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('Liked by'),
        related_name="likes",
        default=None,
        blank=True,
    )
    date_created = models.DateTimeField(
        _('Date created'),
        auto_now_add=True
    )
    latest = models.DateTimeField(
        _('Latest'),
        auto_now=True
    )

    def __str__(self):
        return f"{self.title}-{self.date_created}"

    def open_ticket_count(self):
        return self.tickets.filter(status='open').count()

    def get_manager_name_set(self):
        name_set = []
        for manager in self.manager.all():
            name_set.append(manager.last_name)
            name_set.append(manager.first_name)
        name_set = set(name_set)
        name_set = ' '.join(name_set)
        return name_set

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Ticket(models.Model):
    class Priority(models.TextChoices):
        GREEN = ('low', _('Low'))
        YELLOW = ('medium', _('Medium'))
        RED = ('high', _('High'))

    class Status(models.TextChoices):
        OPEN = ('open', _('Open'))
        ASSIGNED = ('assigned', _('Assigned'))
        CLOSED = ('closed', _('Closed'))

    class Type(models.TextChoices):
        BUGS_ERRORS = ('bugs_errors', _('Bugs/Errors'))
        FEATURE_REQUEST = ('feature_request', _('Feature Request'))
        QUESTIONS = ('questions', _('Questions'))

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_('Project')
    )

    title = models.CharField(
        _('Title'),
        max_length=50
    )

    description = models.TextField(
        _('Description'),
        max_length=500,
    )

    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_submitter_of",
        verbose_name=_('Submitter')
    )

    priority = models.CharField(
        _('Priority'),
        choices=Priority.choices,
        max_length=20
    )

    status = models.CharField(
        _('Status'),
        choices=Status.choices,
        max_length=20,
        default=Status.OPEN
    )

    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=Type.choices
    )

    assign_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(user_deleted),
        related_name="is_assigned_to",
        verbose_name=_('Assignment'),
    )

    date_created = models.DateTimeField(
        _('Date created'),
        auto_now_add=True
    )

    update = models.DateTimeField(
        _('Update'),
        auto_now=True,
    )

    def __str__(self):
        return f'{self.project.name}:{self.pk}'

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_('Ticket')
    )
    body = models.TextField(
        _('Body'),
        blank=True,
        max_length=500,
    )
    date_created = models.DateTimeField(
        _('Date Created'),
        auto_now_add=True
    )
    last_edit = models.DateTimeField(
        _('Last Edit'),
        auto_now=True
    )


def get_image_path(instance, filename):
    return f'comments/{instance.comment.ticket.project.title}/\
        {instance.comment.ticket.id}/\
        {instance.comment.id}/{filename}'


class Attachment(models.Model):
    attach_to = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_('Attach to')
    )
    attachment = models.ImageField(
        _('Attachment'),
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        upload_to=get_image_path
    )
