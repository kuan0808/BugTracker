from django.shortcuts import render
from django.views.generic import ListView
from .models import (
    Project,
    Ticket,
    Comment,
    Attachment,
)


class ProjectListView(ListView):
    pass
