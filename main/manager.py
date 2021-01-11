from django.db import models
from .models import (
    Project,
    Ticket,
    Comment,
    Attachment,
)


class ProjectManager(models.Manager):
    def get_num_tickets(self, project):
        num = Ticket.objects.filter(project=project).count()
        return num
