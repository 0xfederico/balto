from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib import messages
from Configurations.mixins import NoPermissionMessageMixin
from notifications.forms import NotificationForm
from notifications.mixins import MyNotificationsMixin
from notifications.models import Notification, RecipientsUser


class ReadNotificationView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest):
        notification_pk = request.POST.get("notification_pk")
        current_user_pk = request.user.pk
        recipient_read = RecipientsUser.objects.get(notification=notification_pk, user=current_user_pk)
        recipient_read.read = True
        recipient_read.read_at = timezone.now()
        recipient_read.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url


class NotificationCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                             CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notifications/notification_create.html'
    success_message = 'Notification created correctly!'
    permission_required = 'notification.add_notification'
    permission_denied_message = "You don't have permission to create notifications"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        form.save_m2m()  # recipients
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Select at least one user to add from the list")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('notifications:notification-info', kwargs={"pk": self.object.pk})


class NotificationDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                             MyNotificationsMixin, SuccessMessageMixin, DeleteView):
    model = Notification
    template_name = 'notifications/notification_delete.html'
    success_message = 'Notification deleted correctly!'
    permission_required = 'notification.delete_notification'
    permission_denied_message = "You don't have permission to delete notifications"
    success_url = reverse_lazy('notifications:notifications-list')


class NotificationInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Notification
    template_name = 'notifications/notification_info.html'


class NotificationListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    ordering = ['-created']


class NotificationUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                             MyNotificationsMixin, SuccessMessageMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notifications/notification_update.html'
    success_message = 'Notification updated correctly!'
    permission_required = 'notification.update_notification'
    permission_denied_message = "You don't have permission to edit notifications"

    def get_success_url(self):
        return reverse_lazy('notifications:notification-info', kwargs={"pk": self.object.pk})
