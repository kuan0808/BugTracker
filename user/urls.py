from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (UserCreateView,
                    UserLogInView,
                    logout_view,
                    ProfileView)
# from .views import register_view, UserLogInView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView, name='profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
