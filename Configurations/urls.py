"""Balto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Configurations.views import FourZeroFour, Homepage, Calendar
from django.contrib.auth import views as auth_views
from users.views import UserCreationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404-not-found', FourZeroFour.as_view(), name='404-not-found'),
    path('', Homepage.as_view(), name='homepage'),
    path('calendar', Calendar.as_view(), name='calendar'),
    path('animals/', include('animals.urls')),
    path('users/', include('users.urls')),
    path('register/', UserCreationView.as_view(), name='users-register'),
    path('login/', auth_views.LoginView.as_view(), name='users-login'),
    path('logout', auth_views.LogoutView.as_view(), name='users-logout'),
    path('password-reset', auth_views.PasswordResetView.as_view(), name='users-password-reset'),
#   path('password-reset-done', auth_views.PasswordResetDoneView.as_view(), name='users-password-reset-done'),
#   path('password-reset-confirm', auth_views.PasswordResetConfirmView.as_view(), name='users-password-reset-confirm'),
#   path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(), name='users-password-reset-complete'),
    path('password-change', auth_views.PasswordChangeView.as_view(), name='users-password-change'),
#   path('password-change-done', auth_views.PasswordChangeDoneView.as_view(), name='users-password-change-done'),
]
