from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from users.forms import UserForm, GroupForm, UserUpdateForm
from users.mixins import IsResponsibleMixin, ItIsHimself, IsSuperuserMixin
from users.models import UserModel
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.models import Group


# ------------------- USER -------------------
class UserCreateView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, CreateView):

    model = UserModel
    form_class = UserForm
    template_name = 'users/registration/user_create.html'
    success_message = 'User created correctly!'

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, ItIsHimself, SuccessMessageMixin,
                     DeleteView):

    model = UserModel
    form_class = UserForm
    template_name = 'users/user_delete.html'
    success_message = 'User deleted correctly!'
    success_url = reverse_lazy('users:users-list')


class UserInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

    model = UserModel
    template_name = 'users/user_info.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {"username": self.object.username,
                   "user_photo": self.object.photo}
        return self.render_to_response(context)


class UserListView(LoginRequiredMixin, SuccessMessageMixin, ListView):

    model = UserModel
    template_name = 'users/user_list.html'


class UserUpdateView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, ItIsHimself, SuccessMessageMixin,
                     UpdateView):

    model = UserModel
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_message = 'User updated correctly!'

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


# ------------------- GROUP -------------------
class GroupCreateView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, CreateView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_create.html'
    success_message = 'Group created correctly!'

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={"pk": self.object.pk})


class GroupDeleteView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, DeleteView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete.html'
    success_message = 'Group deleted correctly!'
    success_url = reverse_lazy('users:groups-list')


class GroupInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

    model = Group
    template_name = "users/group_info.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {"group_name": self.object.name,
                   "group_permissions": [i.name for i in self.object.permissions.all()]}
        return self.render_to_response(context)


class GroupListView(LoginRequiredMixin, SuccessMessageMixin, ListView):

    model = Group
    template_name = 'users/group_list.html'


class GroupUpdateView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, UpdateView):

    model = Group
    form_class = GroupForm
    template_name = 'users/group_update.html'
    success_message = 'Group updated correctly!'

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={"pk": self.object.pk})

