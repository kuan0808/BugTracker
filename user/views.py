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
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm
)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'user/register_form.html'
    success_url = '/login/'
    success_message = _("User Created !")


class UserLogInView(FormView):
    form_class = UserLoginForm
    template_name = 'user/login_form.html'
    success_url = '/home/'

    def dispatch(self, request, *args, **kwargs):
        """
        Assign request to get method or post method, first method been called.
        """
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data
        user = authenticate(username=credentials['username'],
                            password=credentials['password'])
        if user:
            login(self.request, user)
            messages.success(self.request, _(
                f"Hi {credentials['username']}. Welcome back !"))
            return super().form_valid(form)
        else:
            messages.warning(self.request, _('Log in failed. \
                                please try again'))
            return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


def ProfileView(request):
    if request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Your account has been updated !'))
            return redirect('profile')
    else:
        if request.user.is_authenticated:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, instance=request.user)
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request, 'user/profile.html', context)
        else:
            return redirect('login')
