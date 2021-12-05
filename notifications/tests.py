from django.test import TestCase, Client
from django.urls import reverse_lazy
import re
import os
import django

# without this setup it is not possible to import the app models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configurations.settings')
django.setup()

from django.contrib.auth.models import Permission
from users.models import User
from notifications.models import Notification, RecipientsUser


class ArchitecturalConsistencyTests(TestCase):
    def setUp(self):
        # delete all existing notifications
        for notification in Notification.objects.all():
            notification.delete()

        # delete all existing recipientsuser
        for recipient in RecipientsUser.objects.all():
            recipient.delete()

        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # user creation
        self.user1 = User.objects.create_user(username='user1', email='user1@balto.org', phone='1111111111',
                                              password='hello123hello123')
        self.user2 = User.objects.create_user(username='user2', email='user2@balto.org', phone='2222222222',
                                              password='hello123hello123')
        self.user3 = User.objects.create_user(username='user3', email='user3@balto.org', phone='3333333333',
                                              password='hello123hello123')
        self.user4 = User.objects.create_user(username='user4', email='user4@balto.org', phone='4444444444',
                                              password='hello123hello123')

        # notification creation
        self.notification = Notification.objects.create(title='test',
                                                        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                             "sed do eiusmod tempor incididunt ut labore et  "
                                                             "magna aliqua. Eros donec ac odio tempor. Ut tellus "
                                                             "elementum sagittis vitae et leo duis ut. Tellus orci ac "
                                                             "auctor augue mauris augue neque. Nibh praesent tristique "
                                                             "magna sit amet purus gravida. Euismod lacinia at quis "
                                                             "risus sed. Cum sociis natoque penatibus et magnis. Quis "
                                                             "commodo odio aenean sed adipiscing. Ante in nibh mauris "
                                                             "cursus. Sed enim ut sem viverra aliquet eget sit amet "
                                                             "tellus. Ultricies leo integer malesuada nunc vel risus "
                                                             "commodo viverra maecenas. Vitae proin sagittis nisl "
                                                             "rhoncus mattis rhoncus urna. Nibh praesent tristique "
                                                             "magna sit amet purus gravida. Pellentesque nec nam "
                                                             "aliquam sem et tortor consequat. Vivamus arcu felis "
                                                             "bibendum ut tristique et egestas. Quam elementum pulvinar"
                                                             " etiam non. Dui accumsan sit amet nulla facilisi morbi "
                                                             "tempus iaculis. Egestas dui id ornare arcu odio.",
                                                        creator=self.user1)
        self.notification.save()
        self.notification.recipients.add(self.user2)
        self.notification.recipients.add(self.user3)
        self.notification.recipients.add(self.user4)

    def test_objects_are_instances_of_the_expected_class(self):
        for r in self.notification.recipients.all():
            self.assertTrue(isinstance(r, User), "notification.recipients it does not contain User's instances.")
        for r in RecipientsUser.objects.all():
            self.assertTrue(isinstance(r.user, User), 'RecipientsUser.user it is not an instance of User')
            self.assertTrue(isinstance(r.notification, Notification),
                            'RecipientsUser.notification it is not an instance of Notification')

    def test_cancellation_of_notification(self):
        self.notification.delete()
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, notification=self.notification.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user2.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user3.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user4.pk)
        self.assertIsNotNone(User.objects.get(pk=self.user1.pk))
        self.assertIsNotNone(User.objects.get(pk=self.user2.pk))
        self.assertIsNotNone(User.objects.get(pk=self.user3.pk))
        self.assertIsNotNone(User.objects.get(pk=self.user4.pk))

    def test_cancellation_of_creator(self):
        self.user1.delete()
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, notification=self.notification.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user2.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user3.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user4.pk)
        self.assertIsNotNone(User.objects.get(pk=self.user2.pk))
        self.assertIsNotNone(User.objects.get(pk=self.user3.pk))
        self.assertIsNotNone(User.objects.get(pk=self.user4.pk))

    def test_cancellation_of_recipients(self):
        self.user2.delete()
        self.user3.delete()
        self.user4.delete()
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, notification=self.notification.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user2.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user3.pk)
        self.assertRaises(RecipientsUser.DoesNotExist, RecipientsUser.objects.get, user=self.user4.pk)
        self.assertIsNotNone(User.objects.get(pk=self.user1.pk))
        self.assertIsNotNone(Notification.objects.get(pk=self.notification.pk))
        self.assertEqual(self.notification.recipients.count(), 0, 'not all recipients have been deleted.')


# You may need to add 'testserver' to ALLOWED_HOSTS.
from Configurations.settings import ALLOWED_HOSTS
ALLOWED_HOSTS.append('testserver')


class ViewsTests(TestCase):
    def setUp(self):
        # delete all existing notifications
        for notification in Notification.objects.all():
            notification.delete()

        # delete all existing recipientsuser
        for recipient in RecipientsUser.objects.all():
            recipient.delete()

        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # user creation
        self.user1 = User.objects.create_user(username='user1', email='user1@balto.org', phone='1111111111',
                                              password='hello123hello123')
        self.user2 = User.objects.create_user(username='user2', email='user2@balto.org', phone='2222222222',
                                              password='hello123hello123')
        self.user3 = User.objects.create_user(username='user3', email='user3@balto.org', phone='3333333333',
                                              password='hello123hello123')
        self.user4 = User.objects.create_user(username='user4', email='user4@balto.org', phone='4444444444',
                                              password='hello123hello123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@balto.org', phone='5555555555',
                                                   password='admin')

        # notification creation
        self.notification = Notification.objects.create(title='test',
                                                        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                             "sed do eiusmod tempor incididunt ut labore et  "
                                                             "magna aliqua. Eros donec ac odio tempor. Ut tellus "
                                                             "elementum sagittis vitae et leo duis ut. Tellus orci ac "
                                                             "auctor augue mauris augue neque. Nibh praesent tristique "
                                                             "magna sit amet purus gravida. Euismod lacinia at quis "
                                                             "risus sed. Cum sociis natoque penatibus et magnis. Quis "
                                                             "commodo odio aenean sed adipiscing. Ante in nibh mauris "
                                                             "cursus. Sed enim ut sem viverra aliquet eget sit amet "
                                                             "tellus. Ultricies leo integer malesuada nunc vel risus "
                                                             "commodo viverra maecenas. Vitae proin sagittis nisl "
                                                             "rhoncus mattis rhoncus urna. Nibh praesent tristique "
                                                             "magna sit amet purus gravida. Pellentesque nec nam "
                                                             "aliquam sem et tortor consequat. Vivamus arcu felis "
                                                             "bibendum ut tristique et egestas. Quam elementum pulvinar"
                                                             " etiam non. Dui accumsan sit amet nulla facilisi morbi "
                                                             "tempus iaculis. Egestas dui id ornare arcu odio.",
                                                        creator=self.user1)
        self.notification.save()
        self.notification.recipients.add(self.user2)
        self.notification.recipients.add(self.user3)
        self.notification.recipients.add(self.user4)

        self.admin_notification = Notification.objects.create(title='test-admin', text='test', creator=self.admin)
        self.admin_notification.save()
        self.admin_notification.recipients.add(self.user1)
        self.admin_notification.recipients.add(self.user2)
        self.admin_notification.recipients.add(self.user3)
        self.admin_notification.recipients.add(self.user4)

    # ---------------
    # - Permissions -
    # ---------------
    def test_permissions(self):
        client = Client()
        self.assertTrue(client.login(username='user2', password='hello123hello123'),
                        'The user2 cannot log in to test Notifications permissions.')

        responses = [client.get(reverse_lazy('notifications:notification-create'), follow=True),
                     client.get(reverse_lazy('notifications:notification-delete', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-info', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notifications-list'), follow=True),
                     client.get(reverse_lazy('notifications:notification-update', kwargs={'pk': self.notification.pk}),
                                follow=True)]

        for response in responses:
            self.assertContains(response, "You don\'t have permission to")
            self.assertEqual(response.redirect_chain, [('/', 302)])

        permissions = [Permission.objects.get(codename='add_notification'),
                       Permission.objects.get(codename='change_notification'),
                       Permission.objects.get(codename='view_notification'),
                       Permission.objects.get(codename='delete_notification')]

        for permission in permissions:
            self.user2.user_permissions.add(permission)

        responses = [client.get(reverse_lazy('notifications:notification-create'), follow=True),
                     client.get(reverse_lazy('notifications:notification-delete', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-info', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notifications-list'), follow=True),
                     client.get(reverse_lazy('notifications:notification-update', kwargs={'pk': self.notification.pk}),
                                follow=True)]

        for response in responses:
            self.assertNotContains(response, "You don\'t have permission to")
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    def test_permissions_himself(self):
        # creation of new notifications
        notification2 = Notification.objects.create(title='test', text='test', creator=self.user2)
        notification2.save()
        notification2.recipients.add(self.user1)
        notification2.recipients.add(self.user2)
        notification2.recipients.add(self.user3)
        notification2.recipients.add(self.user4)

        notification3 = Notification.objects.create(title='test-test', text='test', creator=self.user1)
        notification3.save()
        notification3.recipients.add(self.user2)
        notification3.recipients.add(self.user3)

        notification4 = Notification.objects.create(title='test-test-test', text='test', creator=self.user3)
        notification4.save()
        notification4.recipients.add(self.user1)
        notification4.recipients.add(self.user4)

        notification5 = Notification.objects.create(title='test-test-test-test', text='test', creator=self.user1)
        notification5.save()
        notification5.recipients.add(self.user1)

        client = Client()
        self.assertTrue(client.login(username='user3', password='hello123hello123'),
                        'The user3 cannot log in to test Notifications Himself permissions.')

        # unauthorized
        permissions = [Permission.objects.get(codename='view_my_notifications'),
                       Permission.objects.get(codename='change_my_notifications'),
                       Permission.objects.get(codename='delete_my_notifications')]

        for permission in permissions:
            self.user3.user_permissions.add(permission)

        responses = [client.get(reverse_lazy('notifications:notification-delete', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-info', kwargs={'pk': self.notification.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-update', kwargs={'pk': self.notification.pk}),
                                follow=True)]

        pattern = re.compile(r'You are not authorized to (view|modify|delete) notifications of other users!')
        for response in responses:
            self.assertTrue(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertEqual(response.redirect_chain, [('/', 302)])

        # authorized
        responses = [client.get(reverse_lazy('notifications:notification-delete', kwargs={'pk': notification4.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-info', kwargs={'pk': notification4.pk}),
                                follow=True),
                     client.get(reverse_lazy('notifications:notification-update', kwargs={'pk': notification4.pk}),
                                follow=True)]

        for response in responses:
            self.assertFalse(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

        # my notifications or addressed to me notifications
        response = client.get(reverse_lazy('notifications:notifications-list'))
        for notification in response.context_data['object_list']:
            self.assertTrue(notification.creator == self.user3 or self.user3 in notification.recipients.all(),
                            'user3 can see notifications for which he is not authorized!')

    def test_permissions_admin(self):
        client = Client()
        self.assertTrue(client.login(username='user4', password='hello123hello123'),
                        'The user4 cannot log in to test Notifications Admin permissions.')

        # unauthorized
        permissions = [Permission.objects.get(codename='view_my_notifications'),
                       Permission.objects.get(codename='change_my_notifications'),
                       Permission.objects.get(codename='delete_my_notifications'),
                       Permission.objects.get(codename='add_notification'),
                       Permission.objects.get(codename='change_notification'),
                       Permission.objects.get(codename='view_notification'),
                       Permission.objects.get(codename='delete_notification')]

        for permission in permissions:
            self.user4.user_permissions.add(permission)

        responses = [client.get(reverse_lazy('notifications:notification-delete',
                                             kwargs={'pk': self.admin_notification.pk}), follow=True),
                     client.get(reverse_lazy('notifications:notification-info',
                                             kwargs={'pk': self.admin_notification.pk}), follow=True),
                     client.get(reverse_lazy('notifications:notification-update',
                                             kwargs={'pk': self.admin_notification.pk}), follow=True)]

        pattern = re.compile(r'Only a superuser can (modify|delete|view) notifications of a superuser!')
        for response in responses:
            self.assertTrue(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_notification_create_and_update(self):
        client = Client()
        self.user1.user_permissions.add(Permission.objects.get(codename='add_notification'))
        self.user1.user_permissions.add(Permission.objects.get(codename='change_notification'))
        self.user1.user_permissions.add(Permission.objects.get(codename='view_notification'))
        self.assertTrue(client.login(username='user1', password='hello123hello123'),
                        'The user1 cannot log in to test NotificationCreateView and NotificationUpdateView.')

        # notification creation
        response = client.post(reverse_lazy('notifications:notification-create'),
                               {
                                   'title': 'notification1',
                                   'text': 'test',
                                   'recipients': [self.user2.pk, self.user3.pk, self.user4.pk],
                               },
                               follow=True)
        try:
            notification = Notification.objects.get(title='notification1', text='test')
        except Notification.DoesNotExist:
            notification = None
        self.assertIsNotNone(notification, 'The notification was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/notifications/{notification.pk}/notification-info', 302)])

        # update notification
        response = client.post(reverse_lazy('notifications:notification-update', kwargs={'pk': notification.pk}),
                               {
                                   'title': notification.title,
                                   'text': 'updated',
                                   'recipients': [r.pk for r in notification.recipients.all()],
                               },
                               follow=True)
        notification = Notification.objects.get(pk=notification.pk)  # retrieve updated object
        self.assertNotEqual(notification.text, 'test', 'The notification was not updated correctly from the view.')
        self.assertEqual(notification.text, 'updated', 'The notification was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/notifications/{notification.pk}/notification-info', 302)])

    def test_notification_delete(self):
        client = Client()
        self.user1.user_permissions.add(Permission.objects.get(codename='view_notification'))
        self.user1.user_permissions.add(Permission.objects.get(codename='delete_notification'))
        self.assertTrue(client.login(username='user1', password='hello123hello123'),
                        'The user1 cannot log in to test NotificationDeleteView.')
        # delete notification
        response = client.post(reverse_lazy('notifications:notification-delete', kwargs={'pk': self.notification.pk}),
                               follow=True)
        self.assertEqual(response.redirect_chain, [(f'/notifications/notifications-list/', 302)])
        self.assertRaises(Notification.DoesNotExist, Notification.objects.get, pk=self.notification.pk)

    def test_notification_info(self):
        client = Client()
        self.user1.user_permissions.add(Permission.objects.get(codename='view_notification'))
        self.assertTrue(client.login(username='user1', password='hello123hello123'),
                        'The user1 cannot log in to test NotificationInfoView.')
        # info notification
        response = client.get(reverse_lazy('notifications:notification-info', kwargs={'pk': self.notification.pk}))
        self.assertEqual(response.context_data['object'], self.notification, 'The notification does not match.')

    def test_notifications_list(self):
        client = Client()
        self.user1.user_permissions.add(Permission.objects.get(codename='view_notification'))
        self.assertTrue(client.login(username='user1', password='hello123hello123'),
                        'The user1 cannot log in to test NotificationListView.')
        # list notification
        response = client.get(reverse_lazy('notifications:notifications-list'))
        self.assertQuerysetEqual(list(response.context_data['object_list']),
                                 [n for n in Notification.objects.all() if not n.creator.is_superuser],
                                 msg='The notifications do not match.')

    def test_notification_read(self):
        client = Client()
        self.assertTrue(client.login(username='user2', password='hello123hello123'),
                        'The user2 cannot log in to test ReadNotificationView.')
        # read notification
        client.post(reverse_lazy('notifications:read-notification'), {'notification_pk': self.notification.pk},
                    follow=False)
        for r in RecipientsUser.objects.filter(user=self.user2, notification=self.notification):
            self.assertTrue(r.read)
