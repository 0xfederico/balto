from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from users.models import UserModel
from django.contrib.auth.models import Group


class UserForm(UserCreationForm):

    helper = FormHelper()
    helper.form_id = "users_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

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
        fields = ["username", "first_name", "last_name", "email", "phone", "photo", "groups"]


class GroupForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_id = "group_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class GroupAddUserForm(forms.Form):

    helper = FormHelper()
    helper.form_id = "group_add_user_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Add"))

    users = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(),
        queryset=UserModel.objects.all().order_by('last_name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = UserModel.objects.all()
