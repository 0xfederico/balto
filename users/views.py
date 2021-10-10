from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from Configurations.mixins import NoPermissionMessageMixin
from users.forms import GroupForm, GroupAddUserForm, AdminCreateForm, AdminUpdateForm
from users.mixins import ItIsHimselfOrAdminMixin
from users.models import User


# ------------------- USER -------------------
class UserCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     CreateView):
    model = User
    form_class = AdminCreateForm
    success_message = 'User created correctly!'
    permission_required = 'users.add_user'
    permission_denied_message = "You don't have permission to add users"

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ItIsHimselfOrAdminMixin,
                     SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_message = 'User deleted correctly!'
    permission_required = 'users.delete_user'
    permission_denied_message = "You don't have permission to delete users"
    success_url = reverse_lazy('users:users-list')


class UserInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = User
    template_name = 'users/user_info.html'


class UserListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    ordering = ['username']


class UserUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ItIsHimselfOrAdminMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = AdminUpdateForm
    template_name = 'users/user_update.html'
    success_message = 'User updated correctly!'
    permission_required = 'users.change_user'
    permission_denied_message = "You don't have permission to edit users"

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


# ------------------- GROUP -------------------
class GroupCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_create.html'
    success_message = 'Group created correctly!'
    permission_required = 'auth.add_group'
    permission_denied_message = "You don't have permission to create groups"

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={"pk": self.object.pk})


class GroupDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      DeleteView):
    model = Group
    template_name = 'users/group_delete.html'
    success_message = 'Group deleted correctly!'
    permission_required = 'auth.delete_group'
    permission_denied_message = "You don't have permission to delete groups"
    success_url = reverse_lazy('users:groups-list')


class GroupDeleteUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                          DeleteView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete_user.html'
    success_message = 'User removed from Group correctly!'
    permission_required = 'group.delete_users_from_group'
    permission_denied_message = "You don't have permission to delete users from group"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "delete_user": User.objects.get(pk=kwargs["upk"])}
        return self.render_to_response(context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.user_set.remove(kwargs["upk"])
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('users:group-members', kwargs={"pk": self.object.pk})


class GroupAddUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'group.add_users_to_group'
    permission_denied_message = "You don't have permission to add users to group"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.group = Group.objects.filter(pk=kwargs["pk"])[0]
        del kwargs["pk"]  # we just need it to retrieve the group
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request: HttpRequest):
        context = {"group": self.group,
                   "form": GroupAddUserForm(request.GET)}
        return render(request, "users/group_add_user.html", context)

    def post(self, request: HttpRequest):
        form = GroupAddUserForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data.get("users")
            for u in users:
                self.group.user_set.add(u)
            messages.success(request, "User added to Group correctly!")
            return HttpResponseRedirect(reverse('users:group-members', kwargs={"pk": self.group.pk}))
        else:
            messages.error(request, "Select at least one user to add from the list")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url but with errors


class GroupInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Group
    template_name = "users/group_info.html"
    ordering = ['name']


class GroupMembersView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Group
    template_name = 'users/group_members.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "members": User.objects.filter(groups__name=self.object.name).order_by('username')}
        return self.render_to_response(context)


class GroupListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Group
    template_name = 'users/group_list.html'


class GroupUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_update.html'
    success_message = 'Group updated correctly!'
    permission_required = 'auth.change_group'
    permission_denied_message = "You don't have permission to edit groups"

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={"pk": self.object.pk})
