from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import ModelMultipleChoiceField

from Configurations.settings import prohibited_permissions
from users.models import User


# ------------------- USER -------------------
class AdminCreateForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'photo', 'groups']
        widgets = {'groups': forms.CheckboxSelectMultiple}


class AdminUpdateForm(UserChangeForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'photo', 'groups']
        widgets = {'groups': forms.CheckboxSelectMultiple}


class UserUpdateForm(UserChangeForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'photo']


# ------------------- GROUP -------------------
class GroupForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    class ChangedLabelCSMF(ModelMultipleChoiceField):
        def label_from_instance(self, permission):
            return permission.name

    permissions = ChangedLabelCSMF(
        label='Permissions',
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.all().exclude(codename__in=prohibited_permissions),
        help_text='Select the permissions for the members of this group',
        required=False  # useful for creating groups without permissions
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class GroupAddUserForm(forms.Form):
    helper = FormHelper()
    helper.form_method = 'POST'

    # The override is necessary to be able to pass as argument the members of the group
    # and exclude them from the selection
    def __init__(self, *args, **kwargs):
        members = kwargs.pop('members')
        super(GroupAddUserForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(label='Users', widget=forms.CheckboxSelectMultiple,
                                                              queryset=User.objects.all().exclude(
                                                                  pk__in=members).order_by('username'),
                                                              help_text='Select a user to add', required=True)
