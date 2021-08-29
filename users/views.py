from django.urls import reverse_lazy
from users.forms import UserForm
from users.models import UserModel
from django.views.generic import CreateView


class UserCreationView(CreateView):
    model = UserModel
    form_class = UserForm
    template_name = 'registration/register.html'
    success_message = 'User created correctly!'
    success_url = reverse_lazy('users-login')

