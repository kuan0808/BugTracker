from django.shortcuts import render
from .forms import UserRegisterForm
from django.views.generic import (
        CreateView
)
from .models import CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'user/user_form.html'




