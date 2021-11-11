from django.views.generic import TemplateView

from activities.models import Activity
from animals.models import Animal
from facility.models import Box, Area
from users.models import User


class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = Animal.objects.count()
        context['users'] = User.objects.count()
        context['activities'] = Activity.objects.count()
        context['boxes'] = Box.objects.count()
        context['areas'] = Area.objects.count()
        return context


class BadRequest(TemplateView):
    template_name = '400.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 400
        return response


class PermissionDenied(TemplateView):
    template_name = '403.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 403
        return response


class PageNotFound(TemplateView):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class ServerError(TemplateView):
    template_name = '500.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 500
        return response
