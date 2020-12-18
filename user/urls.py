from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (UserCreateView,
                    UserLogInView,
                    logout_view,
                    ProfileView)
# from .views import register_view, UserLogInView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
