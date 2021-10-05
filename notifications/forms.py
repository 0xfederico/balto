from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from notifications.models import Notification
from users.models import UserModel


class NotificationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "notification_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Create"))

    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',
                    '/static/admin/css/responsive.css',
                    # '/static/admin/css/base.css',
                    )
        }
        js = ('/admin/jsi18n/',
              '/static/admin/js/vendor/jquery/jquery.js',
              '/static/admin/js/jquery.init.js',
              '/static/admin/js/core.js',
              )

    recipients = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(verbose_name="Recipient users", is_stacked=False),
        queryset=UserModel.objects.all().order_by('username'),
        help_text='Select a user to add',
        required=True
    )

    class Meta:
        model = Notification
        fields = ["title", "text", "recipients"]
