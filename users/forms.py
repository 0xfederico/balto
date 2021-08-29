from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from users.models import UserModel


class UserForm(UserCreationForm):

    helper = FormHelper()
    helper.form_id = "users_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("save", "Save"))

    class Meta:
        model = UserModel
        fields = ["username", "first_name", "last_name", "email", "phone", "photo"]

