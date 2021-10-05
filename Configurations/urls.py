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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Configurations.views import FourZeroFour, Homepage, Calendar
from django import views as django_views

urlpatterns = [
    url(r'^jsi18n/$', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),  # admin FilteredSelectMultiple
    path('admin/', admin.site.urls),
    path('404-not-found', FourZeroFour.as_view(), name='404-not-found'),
    path('', Homepage.as_view(), name='homepage'),
    path('calendar', Calendar.as_view(), name='calendar'),
    path('animals/', include('animals.urls')),
    path('users/', include('users.urls')),
    path('notifications/', include('notifications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
