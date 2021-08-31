from django.urls import path

from users.views import GroupCreate, GroupUpdate, GroupDelete, GroupList, GroupInfo

app_name = "users"

urlpatterns = [
    path('group-create', GroupCreate.as_view(), name='group-create'),
    path('<int:pk>/group-update', GroupUpdate.as_view(), name='group-update'),
    path('<int:pk>/group-delete', GroupDelete.as_view(), name='group-delete'),
    path('<int:pk>/group-info', GroupInfo.as_view(), name='group-info'),
    path('groups/', GroupList.as_view(), name='group-list'),
]

