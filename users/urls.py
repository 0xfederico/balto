from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users.views import GroupCreateView, GroupUpdateView, GroupDeleteView, GroupListView, \
    GroupInfoView, UserInfoView, UserDeleteView, UserListView, UserUpdateView, UserCreateView, GroupMembersView, \
    GroupDeleteUserView, GroupAddUsersView, GroupDeleteAllUsersView

app_name = 'users'

urlpatterns = [
    # GROUP
    path('group-create', GroupCreateView.as_view(), name='group-create'),
    path('<int:pk>/group-delete', GroupDeleteView.as_view(), name='group-delete'),
    path('<int:pk>/<int:upk>/group-delete-user', GroupDeleteUserView.as_view(), name='group-delete-user'),
    path('<int:pk>/group-delete-all-users', GroupDeleteAllUsersView.as_view(), name='group-delete-all-users'),
    path('<int:pk>/group-add-users', GroupAddUsersView.as_view(), name='group-add-users'),
    path('<int:pk>/group-info', GroupInfoView.as_view(), name='group-info'),
    path('groups-list/', GroupListView.as_view(), name='groups-list'),
    path('<int:pk>/group-members', GroupMembersView.as_view(), name='group-members'),
    path('<int:pk>/group-update', GroupUpdateView.as_view(), name='group-update'),
    # USER
    path('user-create', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/user-delete', UserDeleteView.as_view(), name='user-delete'),
    path('<int:pk>/user-info', UserInfoView.as_view(), name='user-info'),
    path('users-list/', UserListView.as_view(), name='users-list'),
    path('<int:pk>/user-update', UserUpdateView.as_view(), name='user-update'),
    # ACCOUNT MANAGEMENT
    path('login/', auth_views.LoginView.as_view(template_name='users/user_login.html'), name='user-login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/user_logged_out.html'), name='user-logout'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html',
                                               success_url=reverse_lazy('users:user-password-change-done')),
         name='user-password-change'),
    path('password-change-done',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='user-password-change-done'),
]
