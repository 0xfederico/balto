from django.contrib import messages
from django.shortcuts import redirect


class MyNotificationsMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to change or delete the notifications of other users!")
            return redirect('homepage')
