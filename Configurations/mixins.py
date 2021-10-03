# all global mixins will be saved in this file

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone


class NoPermissionMessageMixin(object):
    def handle_no_permission(self):
        messages.error(self.request, self.__class__.permission_denied_message)
        return redirect("homepage")


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
