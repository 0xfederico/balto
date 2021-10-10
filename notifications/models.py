from django.db import models

from Configurations.mixins import CreatedModifiedMixin
from users.models import User


class Notification(CreatedModifiedMixin, models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, through='RecipientsUser')


class RecipientsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
