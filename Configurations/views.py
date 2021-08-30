from django.views.generic import TemplateView


class FourZeroFour(TemplateView):

    template_name = '404.html'


class Homepage(TemplateView):

    template_name = 'home.html'

class Calendar(TemplateView):

    template_name = 'calendar.html'

