from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from users.forms import UserAdminResponsibleCreateForm, GroupForm, GroupAddUserForm, UserAdminResponsibleUpdateForm
from users.mixins import IsResponsibleMixin, ItIsHimselfMixin, IsSuperuserMixin, ItIsHimselfUpdateMixin
from users.models import UserModel
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.models import Group


# ------------------- USER -------------------
class UserCreateView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = UserAdminResponsibleCreateForm
    template_name = 'users/registration/user_create.html'
    success_message = 'User created correctly!'

    def get_success_url(self):
        return reverse_lazy('users:user-info', kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, ItIsHimselfMixin, SuccessMessageMixin,
                     DeleteView):
    model = UserModel
    form_class = UserAdminResponsibleCreateForm
    template_name = 'users/user_delete.html'
    success_message = 'User deleted correctly!'
    success_url = reverse_lazy('users:users-list')


class UserInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = UserModel
    template_name = 'users/user_info.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"object": self.object,
                   "groups": list(self.object.groups.all())}
        return self.render_to_response(context)


class UserListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = UserModel
    template_name = 'users/user_list.html'
    ordering = ['username']


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, ItIsHimselfUpdateMixin, UpdateView):
    model = UserModel
    form_class = UserAdminResponsibleUpdateForm
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


class GroupDeleteUserView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, SuccessMessageMixin, DeleteView):
    model = Group
    form_class = GroupForm
    template_name = 'users/group_delete_user.html'
    success_message = 'User removed from Group correctly!'

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "delete_user": UserModel.objects.get(pk=kwargs["upk"])}
        return self.render_to_response(context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.user_set.remove(kwargs["upk"])
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('users:group-members', kwargs={"pk": self.object.pk})


class GroupAddUserView(LoginRequiredMixin, IsResponsibleMixin, IsSuperuserMixin, View):

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
            messages.error(request, "Select a user from the list")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url but with errors


class GroupInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Group
    template_name = "users/group_info.html"
    ordering = ['name']

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group_name": self.object.name,
                   "group_pk": self.object.pk,
                   "group_permissions": [i.name for i in self.object.permissions.all()]}
        return self.render_to_response(context)


class GroupMembersView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Group
    template_name = 'users/group_members.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {"group": self.object,
                   "members": UserModel.objects.filter(groups__name=self.object.name)}
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
