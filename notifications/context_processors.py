from notifications.models import RecipientsUser


def my_notifications(request):
    unread_notifications_sorted = dict()
    if request.user.is_authenticated:
        unread_notifications = [r.notification for r in
                                RecipientsUser.objects.filter(user=request.user).filter(read=False)]
        unread_notifications_sorted = sorted(unread_notifications, key=lambda n: n.modified, reverse=True)
    return {'mynotifications': unread_notifications_sorted}
