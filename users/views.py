from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from Configurations.mixins import NoPermissionMessageMixin, AnyPermissionsMixin
from users.forms import GroupForm, GroupAddUserForm, AdminCreateForm, AdminUpdateForm
from users.mixins import IsNotAdminUpdateMixin, SaveSelectedUserMixin, HimselfMixin, \
    CanUpdateAdminMixin, CanDeleteAdminMixin
from users.models import User


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


# ------------------- USER -------------------
class UserCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     CreateView):
    model = User
    form_class = AdminCreateForm
    template_name = 'users/user_create_or_update.html'
    success_message = 'User created correctly!'
    permission_required = 'users.add_user'
    permission_denied_message = "You don't have permission to add users"

    def form_valid(self, form):
        self.object = form.save()
        form.save_m2m()  # save groups
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'groups' in form.errors.as_data():  # check if the error is in the groups field
            returned_data_form['groups_error'] = form.fields['groups'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})


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
                   NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_info.html'
    permission_required = ('users.view_profile', 'users.view_user')
    permission_denied_message = "You don't have permission to view this user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = get_user_permissions(self.object)
        return context


class UserListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ListView):
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
    template_name = 'users/user_create_or_update.html'
    success_message = 'User updated correctly!'
    permission_required = ('users.change_profile', 'users.change_user')
    permission_denied_message = "You don't have permission to edit users"

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'groups' in form.errors.as_data():  # check if the error is in the groups field
            returned_data_form['groups_error'] = form.fields['groups'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})


# ------------------- GROUP -------------------
class GroupCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_create_or_update.html'
    success_message = 'Group created correctly!'
    permission_required = 'auth.add_group'
    permission_denied_message = "You don't have permission to create groups"

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'permissions' in form.errors.as_data():  # check if the error is in the permissions field
            returned_data_form['permissions_error'] = form.fields['permissions'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})


class GroupDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      DeleteView):
    model = Group
    template_name = 'users/group_delete.html'
    success_message = 'Group deleted correctly!'
    permission_required = 'auth.delete_group'
    permission_denied_message = "You don't have permission to delete groups"
    success_url = reverse_lazy('users:groups-list')

    # A group cannot be canceled if it has users within it
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        group_users_count = User.objects.filter(groups__name=self.object.name).count()
        if group_users_count > 0:
            message_error = f'There are {group_users_count} users' if group_users_count > 1 else 'There is a user'
            messages.error(request, message_error + ' in this group, it cannot be deleted!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url but with errors
        else:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())


class GroupAddUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'users.group_add_users'
    permission_denied_message = "You don't have permission to add users to group"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.group = get_object_or_404(Group, pk=kwargs['pk'])
        del kwargs['pk']  # we just need it to retrieve the group
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request: HttpRequest):
        context = {'group': self.group,
                   # In the second argument it is passed the list of group members
                   'form': GroupAddUserForm(request.GET, members=[u.pk for u in self.group.user_set.all()])}
        return render(request, 'users/group_add_user.html', context)

    def post(self, request: HttpRequest):
        # In the second argument it is passed the list of group members
        form = GroupAddUserForm(request.POST, members=[u.pk for u in self.group.user_set.all()])
        if form.is_valid():
            users = form.cleaned_data.get('users')
            for u in users:
                self.group.user_set.add(u)
            messages.success(request, 'User added to Group correctly!')
            return HttpResponseRedirect(reverse('users:group-members', kwargs={'pk': self.group.pk}))
        else:
            returned_data_form = dict()
            returned_data_form['group'] = self.group
            returned_data_form['form'] = form
            if 'users' in form.errors.as_data():  # check if the error is in the users field
                returned_data_form['users_error'] = form.fields['users'].error_messages['required']
            return render(self.request, 'users/group_add_user.html', returned_data_form)


class GroupDeleteUserView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                          DeleteView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete_user.html'
    success_message = 'User removed from Group correctly!'
    permission_required = 'users.group_delete_users'
    permission_denied_message = "You don't have permission to delete users from group"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {'group': self.object,
                   'delete_user': get_object_or_404(User, pk=kwargs['upk'])}
        return self.render_to_response(context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.user_set.remove(kwargs['upk'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('users:group-members', kwargs={'pk': self.object.pk})


class GroupDeleteAllUsersView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'users.group_delete_users'
    permission_denied_message = "You don't have permission to delete users from group"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.group = get_object_or_404(Group, pk=kwargs['pk'])
        del kwargs['pk']  # we just need it to retrieve the group
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request: HttpRequest):
        context = {'group': self.group}
        return render(request, 'users/group_delete_all_user.html', context)

    def post(self, request: HttpRequest):
        users = User.objects.filter(groups__name=self.group.name)
        for u in users:
            self.group.user_set.remove(u.pk)
        messages.success(request, 'Removed all users from the group!')
        return HttpResponseRedirect(reverse('users:group-members', kwargs={'pk': self.group.pk}))


class GroupMembersView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = Group
    template_name = 'users/group_members.html'
    permission_required = 'users.group_view_members'
    permission_denied_message = "You don't have permission to see group members"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {'group': self.object,
                   'members': User.objects.filter(groups__name=self.object.name).order_by('username')}
        return self.render_to_response(context)


class GroupInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = Group
    template_name = 'users/group_info.html'
    permission_required = 'auth.view_group'
    permission_denied_message = "You don't have permission to view this group"
    ordering = ['name']


class GroupListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = 'users/group_list.html'
    permission_required = 'auth.view_group'
    permission_denied_message = "You don't have permission to view groups"


class GroupUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                      UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_create_or_update.html'
    success_message = 'Group updated correctly!'
    permission_required = 'auth.change_group'
    permission_denied_message = "You don't have permission to edit groups"

    def get_success_url(self):
        return reverse_lazy('users:group-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'permissions' in form.errors.as_data():  # check if the error is in the permissions field
            returned_data_form['permissions_error'] = form.fields['permissions'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})
