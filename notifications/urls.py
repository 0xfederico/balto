from django.urls import path

from notifications.views import ReadNotificationView, NotificationCreateView, NotificationDeleteView, \
    NotificationInfoView, NotificationListView, NotificationUpdateView

app_name = 'notifications'

urlpatterns = [
    path('read-notification', ReadNotificationView.as_view(), name='read-notification'),
    path('notification-create', NotificationCreateView.as_view(), name='notification-create'),
    path('<int:pk>/notification-delete', NotificationDeleteView.as_view(), name='notification-delete'),
    path('<int:pk>/notification-info', NotificationInfoView.as_view(), name='notification-info'),
    path('notifications-list/', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/notification-update', NotificationUpdateView.as_view(), name='notification-update'),
]
