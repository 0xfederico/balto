from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from users.forms import UserUpdateForm
from users.models import UserModel


class IsResponsibleMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # superuser must also be included in the condition otherwise they can't do anything
        if request.user.is_responsible or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized, contact a responsible!")
            return redirect('homepage')


class IsSuperuserMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized, contact a responsible!")
            return redirect('homepage')


class ItIsHimselfMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            selected_user = UserModel.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('404-not-found')
        # superuser/responsible must also be included in the condition otherwise they cannot modify other users
        if request.user == selected_user or request.user.is_responsible or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to change the accounts of other users!")
            return redirect('homepage')


class ItIsHimselfUpdateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            selected_user = UserModel.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('404-not-found')
        if not (request.user.is_responsible or request.user.is_superuser):
            if request.user == selected_user:
                self.__class__.form_class = UserUpdateForm
            else:
                messages.error(request, "You are not authorized to change the accounts of other users!")
                return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
