from notifications.models import Notification, RecipientsUser


def my_notifications(request):
    unread_notifications = dict()
    if request.user.is_authenticated and request.user.is_active:
        unread_notifications = RecipientsUser.objects.filter(user=request.user).filter(read=False)
    return {'mynotifications': unread_notifications}
