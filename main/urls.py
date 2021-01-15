from django.contrib import admin
from django.urls import path, include
from .views import (ProjectListView,
                    projectLikeUnlike,
                    )

app_name = 'main'

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project-like-unlike/', projectLikeUnlike, name='project-like-unlike'),
]
