from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from users.forms import UserUpdateForm
from users.models import UserModel


class ItIsHimselfOrAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            selected_user = UserModel.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('404-not-found')
        if request.user == selected_user or request.user.is_superuser:
            if not request.user.is_superuser:
                self.__class__.form_class = UserUpdateForm
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to change the accounts of other users!")
            return redirect('homepage')


class NoPermissionMessageMixin(object):
    def handle_no_permission(self):
        messages.error(self.request, self.__class__.permission_denied_message)
        return redirect("homepage")
