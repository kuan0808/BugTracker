from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
        CreateView
)
from .models import CustomUser
from .forms import UserRegisterForm


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'user/user_form.html'
    success_url = '/register/'
    success_message = "User Created !"




