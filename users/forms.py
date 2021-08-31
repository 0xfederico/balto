from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        fields = ["username", "first_name", "last_name", "email", "phone", "photo"]


class GroupForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_id = "group_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

    class Meta:
        model = Group
        fields = ["name", "permissions"]

