from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib import messages
from Configurations.mixins import NoPermissionMessageMixin, AnyPermissionsMixin
from notifications.forms import NotificationForm
from notifications.mixins import HimselfMixin, CanDeleteAdminMixin, CanUpdateAdminMixin, CanViewAdminMixin
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
    template_name = 'notifications/notification_create_or_update.html'
    success_message = 'Notification created correctly!'
    permission_required = 'notifications.add_notification'
    permission_denied_message = "You don't have permission to create notifications"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_text"] = "Create"
        return context

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


class NotificationDeleteView(LoginRequiredMixin, AnyPermissionsMixin, HimselfMixin, CanDeleteAdminMixin,
                             NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Notification
    template_name = 'notifications/notification_delete.html'
    success_message = 'Notification deleted correctly!'
    permission_required = ('notifications.delete_my_notifications', 'notifications.delete_notification')
    permission_denied_message = "You don't have permission to delete notifications"
    success_url = reverse_lazy('notifications:notifications-list')


class NotificationInfoView(LoginRequiredMixin, AnyPermissionsMixin, HimselfMixin, CanViewAdminMixin,
                           NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Notification
    template_name = 'notifications/notification_info.html'
    permission_required = ('notifications.view_my_notifications', 'notifications.view_notification')


class NotificationListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                           SuccessMessageMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    permission_required = 'notifications.view_my_notifications'
    ordering = ['-created']

    def get_queryset(self):
        qs = super().get_queryset()
        my_notifications = qs.filter(creator=self.request.user)
        addressed_to_me_notifications = qs.filter(recipients=self.request.user)
        return (my_notifications | addressed_to_me_notifications).distinct()  # union without duplicates


class NotificationUpdateView(LoginRequiredMixin, AnyPermissionsMixin, HimselfMixin, CanUpdateAdminMixin,
                             NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notifications/notification_create_or_update.html'
    success_message = 'Notification updated correctly!'
    permission_required = ('notifications.change_my_notifications', 'notifications.change_notification')
    permission_denied_message = "You don't have permission to edit notifications"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_text"] = "Update"
        return context

    def get_success_url(self):
        return reverse_lazy('notifications:notification-info', kwargs={"pk": self.object.pk})
