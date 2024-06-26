from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404

from users.forms import UserUpdateForm
from users.models import User


# edit the form to show if the user is not admin
class IsNotAdminUpdateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.has_perm('users.change_user'):
                self.__class__.form_class = UserUpdateForm  # downgraded
        return super().dispatch(request, *args, **kwargs)


# store selected user for others mixins
class SaveSelectedUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.selected_user = get_object_or_404(User, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('404-not-found')
        return super().dispatch(request, *args, **kwargs)


# check if a user is viewing another user's profile
# dependency: SaveSelectedUserMixin
class HimselfInfoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('users.view_profile') and not request.user.has_perm('users.view_user'):
            if request.user == self.selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to view the accounts of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a user is modifying another user's profile
# dependency: SaveSelectedUserMixin
class HimselfUpdateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('users.change_profile') and not request.user.has_perm('users.change_user'):
            if request.user == self.selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to modify the accounts of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a user is deleting another user's profile
# dependency: SaveSelectedUserMixin
class HimselfDeleteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('users.delete_profile') and not request.user.has_perm('users.delete_user'):
            if request.user == self.selected_user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to delete the accounts of other users!')
                return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a non-superuser is trying to update a superuser
# dependency: SaveSelectedUserMixin
class CanUpdateAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.selected_user.is_superuser:
            messages.error(request, 'Only a superuser can modify a superuser!')
            return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)


# check if a non-superuser is trying to delete a superuser
# dependency: SaveSelectedUserMixin
class CanDeleteAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.selected_user.is_superuser:
            messages.error(request, 'Only a superuser can delete a superuser!')
            return redirect('homepage')
        else:
            return super().dispatch(request, *args, **kwargs)
