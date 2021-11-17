# all global mixins will be saved in this file

from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone


class NoPermissionMessageMixin(object):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.__class__.permission_denied_message)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return super().handle_no_permission()


class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    ''' On save, update timestamps '''

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


# change all() to any()
class AnyPermissionsMixin(object):
    def has_permission(self):
        return any(self.request.user.has_perm(p) for p in self.get_permission_required())
