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
from users.mixins import IsNotAdminUpdateMixin, AnyPermissionsMixin, SaveSelectedUserMixin, HimselfMixin,\
    CanUpdateAdminMixin, CanDeleteAdminMixin
from users.models import User


# ------------------- USER -------------------
class UserCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     CreateView):
    model = User
    form_class = AdminCreateForm
    template_name = 'users/user_create.html'
    success_message = 'User created correctly!'
    permission_required = 'users.add_user'
    permission_denied_message = "You don't have permission to add users"

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, AnyPermissionsMixin, SaveSelectedUserMixin, HimselfMixin,
                     CanDeleteAdminMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_message = 'User deleted correctly!'
    permission_required = ('users.delete_profile', 'users.delete_user')
    permission_denied_message = "You don't have permission to delete users"
    success_url = reverse_lazy('users:users-list')


class UserInfoView(LoginRequiredMixin, AnyPermissionsMixin, SaveSelectedUserMixin, HimselfMixin,
                   NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = User
    template_name = 'users/user_info.html'
    permission_required = ('users.view_profile', 'users.view_user')
    permission_denied_message = "You don't have permission to view this user"


class UserListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                   ListView):
    model = User
    template_name = 'users/user_list.html'
    permission_required = 'users.view_user'
    permission_denied_message = "You don't have permission to view users"
    ordering = ['username']


class UserUpdateView(LoginRequiredMixin, IsNotAdminUpdateMixin, AnyPermissionsMixin, SaveSelectedUserMixin,
                     HimselfMixin, CanUpdateAdminMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = AdminUpdateForm
    template_name = 'users/user_update.html'
    success_message = 'User updated correctly!'
    permission_required = ('users.change_profile', 'users.change_user')
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


class GroupAddUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'users.group_add_users_to_group'
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


class GroupDeleteUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                          DeleteView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete_user.html'
    success_message = 'User removed from Group correctly!'
    permission_required = 'users.group_delete_users_from_group'
    permission_denied_message = "You don't have permission to delete users from group"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "delete_user": User.objects.get(pk=kwargs["upk"])}
        return self.render_to_response(context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.user_set.remove(kwargs["upk"])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('users:group-members', kwargs={"pk": self.object.pk})


class GroupMembersView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       DetailView):
    model = Group
    template_name = 'users/group_members.html'
    permission_required = 'users.group_view_members'
    permission_denied_message = "You don't have permission to see group members"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "members": User.objects.filter(groups__name=self.object.name).order_by('username')}
        return self.render_to_response(context)


class GroupInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    DetailView):
    model = Group
    template_name = "users/group_info.html"
    permission_required = 'auth.view_group'
    permission_denied_message = "You don't have permission to view this group"
    ordering = ['name']


class GroupListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    ListView):
    model = Group
    template_name = 'users/group_list.html'
    permission_required = 'auth.view_group'
    permission_denied_message = "You don't have permission to view groups"


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
