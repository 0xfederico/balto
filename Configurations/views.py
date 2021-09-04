from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class FourZeroFour(TemplateView):

    template_name = '404.html'


class Homepage(TemplateView):

    template_name = 'home.html'


class Calendar(LoginRequiredMixin, TemplateView):

    template_name = 'calendar.html'
