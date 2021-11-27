from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import tempfile
import os
import re
import django

# without this setup it is not possible to import the app models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configurations.settings')
django.setup()

from django.contrib.auth.models import Permission
from activities.models import Activity, Event, custom_slugify
from animals.models import Animal
from facility.models import Area, Box
from users.models import User


class ArchitecturalConsistencyTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing activities
        for activity in Activity.objects.all():
            activity.delete()

        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing events
        for event in Event.objects.all():
            event.delete()

        # user creation
        self.user1 = User.objects.create_user(username='user1', email='user1@balto.org', phone='1234567890',
                                              password='hello123123')
        self.user2 = User.objects.create_user(username='user2', email='user2@balto.org', phone='0987654321',
                                              password='hello123123')

        # areas, box, animals creation
        self.area = Area.objects.create(name='testarea')
        self.box = Box.objects.create(name='testbox', located_area=self.area)
        self.animal1 = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=365), box=self.box)
        self.animal2 = Animal.objects.create(name='Lassie', breed='Rough Collie', sex='Female',
                                             microchip=222222222222222,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=182), box=self.box)

        # activity and event creation
        self.activity = Activity.objects.create(name='walk with animals',
                                                action_to_be_performed='take the animals out for a walk',
                                                icon=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.event = Event(datetime=timezone.now(), activity=self.activity, note='everything good!!')
        self.event.save()
        self.event.users.add(self.user1.pk, self.user2.pk)
        self.event.animals.add(self.animal1.pk, self.animal2.pk)

    def tearDown(self):
        tempfile.mkstemp()  # cleaning the created image

    def test_objects_are_instances_of_the_expected_class(self):
        self.assertTrue(isinstance(self.box.located_area, Area), 'box.located_area is not an instance of Area.')
        self.assertTrue(isinstance(self.animal1.box, Box), 'animal1.box is not an instance of Box.')
        self.assertTrue(isinstance(self.animal2.box, Box), 'animal2.box is not an instance of Box.')
        self.assertTrue(isinstance(self.event.activity, Activity), 'event.activity is not an instance of Activity.')
        self.assertEqual(list(self.event.users.all()), list(User.objects.all()), 'users do not match.')
        self.assertEqual(list(self.event.animals.all()), list(Animal.objects.all()), 'animals do not match.')

    def test_remove_special_characters_custom_slugify(self):
        self.assertNotIn('-', custom_slugify(self.activity.name),
                         'there are illegal characters for the permission name')

    def test_activity_created_the_related_permission_successfully(self):
        self.assertTrue(len(Permission.objects.filter(codename=custom_slugify(self.activity.name))) == 1,
                        msg='creating the activity did not generate the related permission')
        self.activity.delete()
        self.assertTrue(len(Permission.objects.filter(codename=custom_slugify(self.activity.name))) == 0,
                        msg='deleting the activity did not remove the related permission')


# You may need to add 'testserver' to ALLOWED_HOSTS.
from Configurations.settings import ALLOWED_HOSTS
ALLOWED_HOSTS.append('testserver')


class ViewsTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing activities
        for activity in Activity.objects.all():
            activity.delete()

        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing events
        for event in Event.objects.all():
            event.delete()

        # user creation
        self.user = User.objects.create_user(username='user', email='user@balto.org', phone='1111111111',
                                             password='hello123hello123')

        # areas, box, animals creation
        self.area = Area.objects.create(name='testarea')
        self.box = Box.objects.create(name='testbox', located_area=self.area)
        self.animal = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                            check_in_date=timezone.now().date() - timedelta(days=20),
                                            birth_date=timezone.now().date() - timedelta(days=365), box=self.box)

        # activity and event creation
        self.activity = Activity.objects.create(name='walk with animals',
                                                action_to_be_performed='take the animals out for a walk',
                                                icon=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.event = Event(datetime=timezone.now(), activity=self.activity, note='everything good!!')
        self.event.save()
        self.event.users.add(self.user.pk)
        self.event.animals.add(self.animal.pk)

    def tearDown(self):
        tempfile.mkstemp()  # cleaning the created image

    # ---------------
    # - Permissions -
    # ---------------
    def test_permissions(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Activities permissions.')
        responses = [client.get(reverse_lazy('activities:activity-create'), follow=True),
                     client.get(reverse_lazy('activities:activity-delete', kwargs={'pk': self.activity.pk}),
                                follow=True),
                     client.get(reverse_lazy('activities:activity-info', kwargs={'pk': self.activity.pk}), follow=True),
                     client.get(reverse_lazy('activities:activities-list'), follow=True),
                     client.get(reverse_lazy('activities:activity-update', kwargs={'pk': self.activity.pk}),
                                follow=True),
                     client.get(reverse_lazy('activities:event-create'), follow=True),
                     client.get(reverse_lazy('activities:event-delete', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:event-info', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:events-list-day'), follow=True),
                     client.get(reverse_lazy('activities:events-list-day', kwargs={'date': '1970-01-01'}), follow=True),
                     client.get(reverse_lazy('activities:event-update', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:search'), follow=True)]

        for response in responses:
            self.assertContains(response, "You don\'t have permission to")
            self.assertEqual(response.redirect_chain, [('/', 302)])

        permissions = [Permission.objects.get(codename='add_activity'),
                       Permission.objects.get(codename='delete_activity'),
                       Permission.objects.get(codename='view_activity'),
                       Permission.objects.get(codename='change_activity'),
                       Permission.objects.get(codename='add_event'),
                       Permission.objects.get(codename='delete_event'),
                       Permission.objects.get(codename='view_event'),
                       Permission.objects.get(codename='change_event'),
                       Permission.objects.get(codename='search')]

        for permission in permissions:
            self.user.user_permissions.add(permission)

        responses = [client.get(reverse_lazy('activities:activity-create'), follow=True),
                     client.get(reverse_lazy('activities:activity-delete', kwargs={'pk': self.activity.pk}),
                                follow=True),
                     client.get(reverse_lazy('activities:activity-info', kwargs={'pk': self.activity.pk}), follow=True),
                     client.get(reverse_lazy('activities:activities-list'), follow=True),
                     client.get(reverse_lazy('activities:activity-update', kwargs={'pk': self.activity.pk}),
                                follow=True),
                     client.get(reverse_lazy('activities:event-create'), follow=True),
                     client.get(reverse_lazy('activities:event-delete', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:event-info', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:events-list-day'), follow=True),
                     client.get(reverse_lazy('activities:events-list-day', kwargs={'date': '1970-01-01'}), follow=True),
                     client.get(reverse_lazy('activities:event-update', kwargs={'pk': self.event.pk}), follow=True),
                     client.get(reverse_lazy('activities:search'), follow=True)]

        for response in responses:
            self.assertNotContains(response, "You don\'t have permission to")
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    # ----------------
    # --- Activity ---
    # ----------------
    def test_activity_create_and_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_activity'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_activity'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_activity'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test ActivityCreateView and ActivityUpdateView.')

        # *valid* image creation
        from binascii import a2b_base64
        binary_data = a2b_base64('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAQAAAABbAUdZAAAABGdBTUEAALGPC'
                                 '/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3Ccul'
                                 'E8AAAAAnRSTlMAAHaTzTgAAAACYktHRAAB3YoTpAAAAAd0SU1FB+ULGA4MMOj'
                                 'SPFoAAAAMSURBVAjXY2AY3AAAAKAAAWElfUcAAAAldEVYdGRhdGU6Y3JlYXRl'
                                 'ADIwMjEtMTEtMjRUMTQ6MTI6NDgrMDA6MDCGVKHsAAAAJXRFWHRkYXRlOm1vZ'
                                 'GlmeQAyMDIxLTExLTI0VDE0OjEyOjQ4KzAwOjAw9wkZUAAAAABJRU5ErkJggg==')
        f = open('image.png', 'wb')
        f.write(binary_data)
        f.close()

        # activity creation
        f = open('image.png', 'rb')
        response = client.post(reverse_lazy('activities:activity-create'),
                               {
                                   'name': 'give food',
                                   'action_to_be_performed': 'give food to animals',
                                   'icon ': f
                               },
                               format='multipart', follow=True)
        f.close()
        try:
            activity = Activity.objects.get(name='give food', action_to_be_performed='give food to animals')
        except Activity.DoesNotExist:
            activity = None
        self.assertIsNotNone(activity, 'The activity was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/activities/{activity.pk}/activity-info', 302)])

        # update activity
        response = client.post(reverse_lazy('activities:activity-update', kwargs={'pk': activity.pk}),
                               {
                                   'name': 'give food and water',
                                   'action_to_be_performed': 'give food and water to animals',
                               },
                               format='multipart', follow=True)
        activity = Activity.objects.get(pk=activity.pk)  # retrieve updated object
        self.assertNotEqual(activity.name, 'give food', 'The activity was not updated correctly from the view.')
        self.assertNotEqual(activity.action_to_be_performed, 'give food to animals',
                            'The activity was not updated correctly from the view.')
        self.assertEqual(activity.name, 'give food and water', 'The activity was not updated correctly from the view.')
        self.assertEqual(activity.action_to_be_performed, 'give food and water to animals',
                         'The activity was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/activities/{activity.pk}/activity-info', 302)])

        # cleaning
        os.remove('image.png')

    def test_activity_delete(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_activity'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_activity'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test ActivityDeleteView.')
        # delete activity
        response = client.post(reverse_lazy('activities:activity-delete', kwargs={'pk': self.activity.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/activities/activities-list/', 302)])
        self.assertRaises(Activity.DoesNotExist, Activity.objects.get, pk=self.activity.pk)

    def test_activity_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_activity'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test ActivityInfoView.')
        # info activity
        response = client.get(reverse_lazy('activities:activity-info', kwargs={'pk': self.activity.pk}))
        self.assertEqual(response.context_data['object'], self.activity, 'The activity does not match.')

    def test_activities_list(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_activity'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test ActivityListView.')
        # list activity
        response = client.get(reverse_lazy('activities:activities-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], Activity.objects.all(),
                                 msg='The activities do not match.')

    # --------------
    # --- Events ---
    # --------------
    def test_event_create_and_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_event'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_event'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_event'))
        self.user.user_permissions.add(Permission.objects.get(codename=custom_slugify(self.activity.name)))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test EventCreateView and EventUpdateView.')

        # event creation
        datetime = timezone.now() - timedelta(days=1)
        response = client.post(reverse_lazy('activities:event-create'),
                               {
                                   'datetime': datetime,
                                   'animals': self.animal.pk,
                                   'users': self.user.pk,
                                   'activity': self.activity.pk,
                                   'note': ''
                               },
                               follow=True)
        try:
            event = Event.objects.get(datetime=datetime, animals=self.animal, users=self.user, activity=self.activity)
        except Event.DoesNotExist:
            event = None
        self.assertIsNotNone(event, 'The event was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/activities/{event.pk}/event-info', 302)])

        # update event
        new_datetime = timezone.now() - timedelta(days=2)
        response = client.post(reverse_lazy('activities:event-update', kwargs={'pk': event.pk}),
                               {
                                   'datetime': new_datetime,
                                   'animals': self.animal.pk,
                                   'users': self.user.pk,
                                   'activity': self.activity.pk,
                                   'note': 'edited'
                               },
                               follow=True)
        event = Event.objects.get(pk=event.pk)  # retrieve updated object
        self.assertNotEqual(event.datetime, datetime, 'The event was not updated correctly from the view.')
        self.assertNotEqual(event.note, '', 'The event was not updated correctly from the view.')
        self.assertEqual(event.datetime, new_datetime, 'The event was not updated correctly from the view.')
        self.assertEqual(event.note, 'edited', 'The event was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/activities/{event.pk}/event-info', 302)])

    def test_event_create_future_date_and_without_activity_permission(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_event'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_event'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_event'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test EventCreateView and EventUpdateView -> future date'
                        ' + no activity permission.')

        # activity objects inputs
        pattern = re.compile(r'<input type="radio" name="activity" value="\d" id="id_activity_\d" required checked>')

        # event creation
        datetime = timezone.now() + timedelta(days=1)
        response = client.post(reverse_lazy('activities:event-create'),
                               {
                                   'datetime': datetime,
                                   'animals': self.animal.pk,
                                   'users': self.user.pk,
                                   'activity': self.activity.pk,
                                   'note': ''
                               },
                               follow=True)
        self.assertContains(response, 'The datetime cannot be in the future.')
        self.assertFalse(pattern.search(re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))))

        # give permission and retry the tests (no future datetime)
        self.user.user_permissions.add(Permission.objects.get(codename=custom_slugify(self.activity.name)))
        datetime = timezone.now()
        response = client.post(reverse_lazy('activities:event-create'),
                               {
                                   'datetime': datetime,
                                   #'animals': self.animal.pk, -> ERROR to avoid redirect!
                                   #'users': self.user.pk, -> ERROR to avoid redirect!
                                   'activity': self.activity.pk,
                                   'note': ''
                               },
                               follow=True)
        self.assertNotContains(response, 'The datetime cannot be in the future.')
        self.assertTrue(pattern.search(re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))))

    def test_event_delete(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_event'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_event'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test EventDeleteView.')
        # delete event
        response = client.post(reverse_lazy('activities:event-delete', kwargs={'pk': self.event.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/activities/events-list/', 302)])
        self.assertRaises(Event.DoesNotExist, Event.objects.get, pk=self.event.pk)

    def test_event_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_event'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test EventInfoView.')
        # info event
        response = client.get(reverse_lazy('activities:event-info', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.context_data['object'], self.event, 'The event does not match.')

    def test_search_context(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='search'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test SearchView.')
        # search events
        response = client.get(reverse_lazy('activities:search'))
        self.assertQuerysetEqual(response.context_data['events'], Event.objects.all(), msg='The events do not match.')
