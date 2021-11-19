from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from datetime import date
from datetime import timedelta

from activities.models import Event, Activity
from animals.models import Animal


class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Events number in the last week
        today = date.today()
        last_week = sorted([str(today - timedelta(days=i)) for i in range(0, 7)])
        last_week_events = [len(Event.objects.filter(datetime__date=day)) for day in last_week]
        context['dates'] = last_week
        context['eventsnumber'] = last_week_events

        # Number of events per activities in the last week
        activities = sorted([i.name for i in Activity.objects.all()])
        events_per_activity = [len(Event.objects.filter(activity__name=activity,
                                                        datetime__range=[timezone.now() - timedelta(days=7),
                                                                         timezone.now()]))
                               for activity in activities]
        context['activities'] = activities
        context['eventsactivity'] = events_per_activity

        # Number of activities made per animal today
        animals = sorted([(i.pk, i.name) for i in Animal.objects.all()], key=lambda k: k[1])
        activities_per_animal_today = [len(Event.objects.filter(datetime__date=date.today(),
                                                                animals=animal[0])) for animal in animals]
        context['animals'] = [j[1] for j in animals]
        context['activitiesnumber'] = activities_per_animal_today
        return context


def handler400(request, *args, **kwargs):
    return render(request, '400.html', context={}, status=400)


def handler403(request, *args, **kwargs):
    return render(request, '403.html', context={}, status=403)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', context={}, status=404)


def handler500(request, *args, **kwargs):
    return render(request, '500.html', context={}, status=500)
