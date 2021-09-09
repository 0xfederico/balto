from django.contrib import messages
from django.shortcuts import redirect


class NoPermissionMessageMixin(object):
    def handle_no_permission(self):
        messages.error(self.request, self.__class__.permission_denied_message)
        return redirect("homepage")
