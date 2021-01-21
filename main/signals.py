from django.db.models.signals import post_save
from .models import (
    Ticket,
    Project,
    Comment,
    Attachment,
)
from django.dispatch import receiver
