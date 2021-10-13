from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from users.forms import UserUpdateForm
from users.models import User


# edit the form to show if the user is not admin
class IsNotAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.has_perms('users.change_user'):
            self.__class__.form_class = UserUpdateForm
        return super().dispatch(request, *args, **kwargs)


# change all() to any()
class AnyPermissions(object):
    def has_permission(self):
        return any(self.request.user.has_perm(p) for p in self.get_permission_required())


# check if a user is viewing/editing/deleting another user's profile
class Himself(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            selected_user = User.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('404-not-found')

        if request.user.has_perm('users.view_profile') and not request.user.has_perm('users.view_user'):
            if request.user == selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authorized to view the accounts of other users!")
                return redirect('homepage')
        elif request.user.has_perm('users.change_profile') and not request.user.has_perm('users.change_user'):
            if request.user == selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authorized to edit the accounts of other users!")
                return redirect('homepage')
        elif request.user.has_perm('users.delete_profile') and not request.user.has_perm('users.delete_user'):
            if request.user == selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authorized to delete the accounts of other users!")
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)
