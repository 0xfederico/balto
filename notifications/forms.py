from crispy_forms.helper import FormHelper
from django import forms

from notifications.models import Notification
from users.models import User


class NotificationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"

    recipients = forms.ModelMultipleChoiceField(
        label="Recipient users",
        widget=forms.CheckboxSelectMultiple,
        queryset=User.objects.all().order_by('username'),
        help_text='Select a user to add',
        required=True
    )

    class Meta:
        model = Notification
        fields = ["title", "text", "recipients"]
