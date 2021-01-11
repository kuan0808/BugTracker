from django.contrib import admin
from django.urls import path, include
from .views import (projectListView,
                    )

app_name = 'main'

urlpatterns = [
    path('projects/', projectListView, name='project-list'),
]
