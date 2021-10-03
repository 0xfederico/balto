from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission

from Configurations.settings import prohibited_permissions
from users.models import UserModel


# ------------------- USER -------------------
class AdminCreateForm(UserCreationForm):
    helper = FormHelper()
    helper.form_id = "users_crispy_form"
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

    groups = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(verbose_name="Groups", is_stacked=False),
        queryset=Group.objects.all().order_by('name'),
        help_text='Select the groups where the user will belong'
    )

    class Meta:
        model = UserModel
        fields = ["username", "first_name", "last_name", "email", "phone", "photo", "groups"]


class AdminUpdateForm(UserChangeForm):
    helper = FormHelper()
    helper.form_id = "user_update_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

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

    password = None

    groups = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(verbose_name="Groups", is_stacked=False),
        queryset=Group.objects.all().order_by('name'),
        help_text='Select the groups where the user will belong'
    )

    class Meta:
        model = UserModel
        fields = ["username", "first_name", "last_name", "email", "phone", "photo", "groups"]


class UserUpdateForm(UserChangeForm):
    helper = FormHelper()
    helper.form_id = "user_update_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

    password = None

    class Meta:
        model = UserModel
        fields = ["username", "first_name", "last_name", "email", "phone", "photo"]


# ------------------- GROUP -------------------
class GroupForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "group_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

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

    permissions = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(verbose_name="Permissions", is_stacked=False),
        queryset=Permission.objects.all().exclude(codename__in=prohibited_permissions),
        help_text='Select the permissions for the members of this group'
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class GroupAddUserForm(forms.Form):
    helper = FormHelper()
    helper.form_id = "group_add_user_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Add"))

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

    users = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(verbose_name="Users", is_stacked=False),
        queryset=UserModel.objects.all().order_by('username'),
        help_text='Select the user to add'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = UserModel.objects.all()
