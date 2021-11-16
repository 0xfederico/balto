import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView, TemplateView
from animals.models import Animal
from Configurations.mixins import NoPermissionMessageMixin
from activities.models import Activity, Event, custom_slugify
from activities.forms import ActivityFormCreate, ActivityFormUpdate, EventForm
from django.contrib.auth.models import Group, Permission


# ------------------- Activities -------------------
class ActivityCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                         CreateView):
    model = Activity
    form_class = ActivityFormCreate
    template_name = 'activities/activity_create_or_update.html'
    success_message = 'Activity created correctly!'
    permission_required = 'activities.add_activity'
    permission_denied_message = "You don't have permission to add activities"

    def get_success_url(self):
        return reverse_lazy('activities:activity-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context


class ActivityDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                         DeleteView):
    model = Activity
    template_name = 'activities/activity_delete.html'
    success_message = 'Activity deleted correctly!'
    permission_required = 'activities.delete_activity'
    permission_denied_message = "You don't have permission to delete activities"
    success_url = reverse_lazy('activities:activities-list')


class ActivityInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       DetailView):
    model = Activity
    template_name = 'activities/activity_info.html'
    permission_required = 'activities.view_activity'
    permission_denied_message = "You don't have permission to view this activity"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(
            permissions=Permission.objects.get(codename=custom_slugify(self.object.name)))
        return context


class ActivityListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    permission_required = 'activities.view_activity'
    permission_denied_message = "You don't have permission to view activities"
    ordering = ['name']


class ActivityUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                         UpdateView):
    model = Activity
    form_class = ActivityFormUpdate
    template_name = 'activities/activity_create_or_update.html'
    success_message = 'Activity updated correctly!'
    permission_required = 'activities.change_activity'
    permission_denied_message = "You don't have permission to edit activities"

    def get_success_url(self):
        return reverse_lazy('activities:activity-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context


# ------------------- Events -------------------
class EventCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      CreateView):
    model = Event
    form_class = EventForm
    template_name = 'activities/event_create_or_update.html'
    success_message = 'Event created correctly!'
    permission_required = 'activities.add_event'
    permission_denied_message = "You don't have permission to add events"
    success_url = reverse_lazy('activities:events-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'animals' in form.errors.as_data():
            returned_data_form['animals_error'] = form.fields['animals'].error_messages['required']
        if 'users' in form.errors.as_data():
            returned_data_form['users_error'] = form.fields['users'].error_messages['required']
        if 'activity' in form.errors.as_data():
            returned_data_form['activity_error'] = form.fields['activity'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['currentuser'] = self.request.user
        return kwargs


class EventDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      DeleteView):
    model = Event
    template_name = 'activities/event_delete.html'
    success_message = 'Event deleted correctly!'
    permission_required = 'activities.delete_event'
    permission_denied_message = "You don't have permission to delete events"
    success_url = reverse_lazy('activities:events-list')


class EventInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    DetailView):
    model = Event
    template_name = 'activities/event_info.html'
    permission_required = 'activities.view_event'
    permission_denied_message = "You don't have permission to view this event"


class ChooseDayView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    TemplateView):
    template_name = 'activities/event_list.html'
    permission_required = 'activities.view_event'
    permission_denied_message = "You don't have permission to view events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = Animal.objects.all()
        return context


class RetrieveDayActivitiesView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                                SuccessMessageMixin, View):
    permission_required = 'activities.view_event'
    permission_denied_message = "You don't have permission to view events"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        data = []
        events = Event.objects.filter(datetime__date=kwargs['date'])
        for event in events:
            information = dict()
            information['animals'] = [i.pk for i in event.animals.all()]
            information['activity'] = event.activity.icon.url
            information['event'] = reverse_lazy('activities:event-info', kwargs={'pk': event.pk})
            data.append(information)
        return HttpResponse(json.dumps(data, indent=4, sort_keys=False, default=str), content_type="application/json")


class EventUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'activities/event_create_or_update.html'
    success_message = 'Event updated correctly!'
    permission_required = 'activities.change_event'
    permission_denied_message = "You don't have permission to edit events"
    success_url = reverse_lazy('activities:events-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'animals' in form.errors.as_data():
            returned_data_form['animals_error'] = form.fields['animals'].error_messages['required']
        if 'users' in form.errors.as_data():
            returned_data_form['users_error'] = form.fields['users'].error_messages['required']
        if 'activity' in form.errors.as_data():
            returned_data_form['activity_error'] = form.fields['activity'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['currentuser'] = self.request.user
        return kwargs
