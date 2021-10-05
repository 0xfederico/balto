from django.db import models

from Configurations.mixins import CreatedModifiedMixin
from users.models import UserModel


class Notification(CreatedModifiedMixin, models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    creator = models.ForeignKey(UserModel, related_name="creator", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(UserModel, through='RecipientsUser')


class RecipientsUser(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
