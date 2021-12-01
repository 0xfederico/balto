from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
from django.utils.text import slugify
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from Configurations.mixins import CreatedModifiedMixin
from animals.models import Animal
from users.models import User


def custom_slugify(value, separator='_'):
    return slugify(value).replace('-', separator)


def activity_directory_path(self, filename):
    return f'activities_{self.pk}_{date.today()}_{filename}'


class Activity(CreatedModifiedMixin, models.Model):
    name = models.CharField(max_length=100)
    action_to_be_performed = models.CharField(max_length=255)
    icon = models.ImageField(upload_to=activity_directory_path,
                             help_text='Choose an icon to represent the activity')

    # this method is not implemented by default in models
    def __str__(self):
        return self.name

    # dynamic creation/update of an Activity's permissions
    def save(self, *args, **kwargs):
        is_new_object = self.pk is None
        old_name = get_object_or_404(Activity, pk=self.pk).name if not is_new_object else None  # avoid exception
        super().save(*args, **kwargs)
        if is_new_object:
            Permission.objects.create(codename=custom_slugify(self.name), name=f'Can {self.action_to_be_performed}',
                                      content_type=get_object_or_404(ContentType, app_label='activities',
                                                                     model='activity'))
        else:
            permission_to_edit = get_object_or_404(Permission, codename=custom_slugify(old_name))
            permission_to_edit.codename = custom_slugify(self.name)
            if str(self.action_to_be_performed).startswith('Can '):
                permission_to_edit.name = self.action_to_be_performed
            else:
                permission_to_edit.name = f'Can {self.action_to_be_performed}'
            permission_to_edit.save()

    # dynamic deletion of an Activity's permissions
    def delete(self, *args, **kwargs):
        old_name = get_object_or_404(Activity, pk=self.pk).name
        super().delete(*args, **kwargs)
        Permission.objects.filter(codename=custom_slugify(old_name)).delete()

    class Meta:
        ordering = ['name']


class Event(CreatedModifiedMixin, models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    animals = models.ManyToManyField(Animal, related_name='events')
    users = models.ManyToManyField(User, related_name='events')
    activity = models.ForeignKey(Activity, related_name='events', on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-datetime']
        permissions = (('search', 'Can do research in events'),)  # added to defaults
