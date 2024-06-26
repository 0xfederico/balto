from django.contrib import messages
from django.shortcuts import redirect


# check if a user is viewing another user's notifications
class HimselfInfoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('notifications.view_my_notifications') and not request.user.has_perm(
                'notifications.view_notification'):
            if request.user == self.get_object().creator or request.user.is_superuser or\
                    request.user in self.get_object().recipients.all():
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to view notifications of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a user is modifying another user's notifications
class HimselfUpdateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('notifications.change_my_notifications') and not request.user.has_perm(
                'notifications.change_notification'):
            if request.user == self.get_object().creator or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to modify notifications of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a user is deleting another user's notifications
class HimselfDeleteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('notifications.delete_my_notifications') and not request.user.has_perm(
                'notifications.delete_notification'):
            if request.user == self.get_object().creator or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to delete notifications of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a non-superuser is trying to update notifications of a superuser
class CanUpdateAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.get_object().creator.is_superuser:
            messages.error(request, 'Only a superuser can modify notifications of a superuser!')
            return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a non-superuser is trying to delete notifications of a superuser
class CanDeleteAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.get_object().creator.is_superuser:
            messages.error(request, 'Only a superuser can delete notifications of a superuser!')
            return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a non-superuser is trying to view notifications of a superuser
class CanViewAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.get_object().creator.is_superuser and\
                request.user not in self.get_object().recipients.all():
            messages.error(request, 'Only a superuser can view notifications of a superuser!')
            return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)
