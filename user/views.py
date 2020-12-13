from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    FormView
)
from django.contrib.auth import login, authenticate, logout
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser
from .forms import UserRegisterForm, UserLoginForm


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'user/register_form.html'
    success_url = '/login/'
    success_message = _("User Created !")


class UserLogInView(FormView):
    form_class = UserLoginForm
    template_name = 'user/login_form.html'
    success_url = 'home'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data
        user = authenticate(username=credentials['username'],
                            password=credentials['password'])
        if user:
            login(self.request, user)
            messages.success(self.request, _(
                f"Hi {credentials['username']}. Welcome back !"))
            return redirect(self.success_url)
        else:
            messages.warning(self.request, _('Log in failed. \
                                please try again'))
            return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')
