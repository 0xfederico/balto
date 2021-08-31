from django.urls import reverse_lazy
from users.forms import UserForm, GroupForm
from users.models import UserModel
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.models import Group


class UserCreationView(CreateView):
    model = UserModel
    form_class = UserForm
    template_name = 'registration/register.html'
    success_message = 'User created correctly!'
    success_url = reverse_lazy('users-login')


class GroupCreate(CreateView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_create.html'
    success_message = 'Group created correctly!'
    success_url = reverse_lazy('homepage')


class GroupUpdate(UpdateView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_update.html'
    success_message = 'Group updated correctly!'
    success_url = reverse_lazy('homepage')


class GroupDelete(DeleteView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete.html'
    success_message = 'Group deleted correctly!'
    success_url = reverse_lazy('homepage')


class GroupList(ListView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_list.html'
    success_url = reverse_lazy('homepage')


class GroupInfo(DetailView):

    model = Group
    template_name = "users/group_info.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        #context = self.get_context_data(object=self.object)
        context = {"group_name": self.object.name,
                   "group_permissions": [i.name for i in self.object.permissions.all()]}
        return self.render_to_response(context)

