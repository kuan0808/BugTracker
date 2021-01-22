from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import login, authenticate, logout
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    FormView
)
from .models import CustomUser, Profile
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm
)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = '/login/'
    success_message = _("User Created !")


class UserLogInView(FormView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    success_url = '/profile/'

    def dispatch(self, request, *args, **kwargs):
        """
        Assign request to get method or post method, first method been called.
        """
        if request.user.is_authenticated:
            return redirect('user:profile')
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('user:login')


@login_required
def profileView(request):
    user_data = (request.POST or None)
    profile_data = (request.FILES or None)
    u_form = UserUpdateForm(user_data, instance=request.user)
    p_form = ProfileUpdateForm(
        user_data, profile_data, instance=request.user.profile)

    if request.is_ajax():
        if p_form.is_valid():
            p_form.save()

    if u_form.is_valid():
        u_form.save()
        messages.success(request, _('Your account has been updated !'))
        return redirect('user:profile')
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/profile.html', context)


@login_required
def avatar_delete(request):
    if request.is_ajax():
        data = {}
        user = request.user
        obj = Profile.objects.filter(user=user)[0]
        obj.image = 'default.png'
        obj.save(update_fields=['image'])
        data["status"] = "Avatar has been deleted !"
        data["default_image_url"] = obj.get_absolute_image_url
        return JsonResponse(data, safe=False)
