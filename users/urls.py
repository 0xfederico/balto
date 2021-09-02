from django.urls import path

from users.views import GroupCreateView, GroupUpdateView, GroupDeleteView, GroupListView, \
    GroupInfoView, UserInfoView, UserDeleteView, UserListView, UserUpdateView, UserCreateView

from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    # GROUP
    path('group-create', GroupCreateView.as_view(), name='group-create'),
    path('<int:pk>/group-delete', GroupDeleteView.as_view(), name='group-delete'),
    path('<int:pk>/group-info', GroupInfoView.as_view(), name='group-info'),
    path('groups-list/', GroupListView.as_view(), name='groups-list'),
    path('<int:pk>/group-update', GroupUpdateView.as_view(), name='group-update'),
    # USER
    path('user-create', UserCreateView.as_view(template_name='users/user_create.html'), name='user-create'),
    path('<int:pk>/user-delete', UserDeleteView.as_view(), name='user-delete'),
    path('<int:pk>/user-info', UserInfoView.as_view(), name='user-info'),
    path('users-list/', UserListView.as_view(), name='users-list'),
    path('<int:pk>/user-update', UserUpdateView.as_view(), name='user-update'),
    # ACCOUNT MANAGEMENT
    path('login/', auth_views.LoginView.as_view(template_name='users/user_login.html'), name='user-login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/user_logged_out.html'), name='user-logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'),
         name='user-password-reset'),
    path('password-reset-done',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='user-password-reset-done'),
    path('password-reset-confirm',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='user-password-reset-confirm'),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='user-password-reset-complete'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'),
         name='user-password-change'),
    path('password-change-done',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='user-password-change-done'),
]

