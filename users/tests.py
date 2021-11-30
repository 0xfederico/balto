from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse_lazy
import os
import re
import django

# without this setup it is not possible to import the app models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configurations.settings')
django.setup()

from django.contrib.auth.models import Permission, Group
from users.models import User


class ArchitecturalConsistencyTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing groups
        for group in Group.objects.all():
            group.delete()

        self.group = Group.objects.create(name='testgroup')
        self.user = User.objects.create_user(username='user', email='user@balto.org', phone='1111111111',
                                             password='hello123hello123')
        self.group.user_set.add(self.user)

    def test_user_username(self):
        self.assertRaises(IntegrityError, User.objects.create_user, username='user', email='user2@balto.org',
                          phone='2222222222', password='hello123hello123')

    def test_user_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, username='user2', email='user@balto.org',
                          phone='2222222222', password='hello123hello123')

    def test_user_phone(self):
        self.assertRaises(IntegrityError, User.objects.create_user, username='user2', email='user2@balto.org',
                          phone='1111111111', password='hello123hello123')

    def test_group_instances(self):
        for grp in self.user.groups.all():
            self.assertTrue(isinstance(grp, Group), 'user groups are not group instances.')
        for usr in self.group.user_set.all():
            self.assertTrue(isinstance(usr, User), 'group members are not a user instance.')

    def test_group_permissions(self):
        permission = Permission.objects.get(codename='add_user')
        self.group.permissions.add(permission)
        self.assertTrue(permission in self.group.permissions.all(), 'permissions are not properly added to a group.')


# You may need to add 'testserver' to ALLOWED_HOSTS.
from Configurations.settings import ALLOWED_HOSTS
ALLOWED_HOSTS.append('testserver')


class ViewsTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing groups
        for group in Group.objects.all():
            group.delete()

        self.group = Group.objects.create(name='testgroup')
        self.user = User.objects.create_user(username='user', email='user@balto.org', phone='1111111111',
                                             password='hello123hello123')
        self.user_test = User.objects.create_user(username='user_test', email='user_test@balto.org', phone='0000000000',
                                                  password='hello123hello123')
        self.admin = User.objects.create_superuser(username='admin', email='admin@balto.org', phone='9999999999',
                                                   password='admin')
        self.group.user_set.add(self.user)

    # ---------------
    # - Permissions -
    # ---------------
    def test_permissions_group(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Users permissions.')

        responses = [client.get(reverse_lazy('users:user-create'), follow=True),
                     client.get(reverse_lazy('users:user-delete', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:users-list'), follow=True),
                     client.get(reverse_lazy('users:user-update', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:group-create'), follow=True),
                     client.get(reverse_lazy('users:group-delete', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-delete-user',
                                             kwargs={'pk': self.group.pk, 'upk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:group-delete-all-users', kwargs={'pk': self.group.pk}),
                                follow=True),
                     client.get(reverse_lazy('users:group-add-users', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-info', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:groups-list'), follow=True),
                     client.get(reverse_lazy('users:group-members', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-update', kwargs={'pk': self.group.pk}), follow=True)]

        for response in responses:
            self.assertContains(response, "You don\'t have permission to")
            self.assertEqual(response.redirect_chain, [('/', 302)])

        permissions = [
            Permission.objects.get(codename='add_user'),
            Permission.objects.get(codename='view_user'),
            Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='delete_user'),
            Permission.objects.get(codename='add_group'),
            Permission.objects.get(codename='view_group'),
            Permission.objects.get(codename='change_group'),
            Permission.objects.get(codename='delete_group'),
            Permission.objects.get(codename='group_add_users'),
            Permission.objects.get(codename='group_delete_users'),
            Permission.objects.get(codename='group_view_members')]

        for permission in permissions:
            self.group.permissions.add(permission)

        responses = [client.get(reverse_lazy('users:user-create'), follow=True),
                     client.get(reverse_lazy('users:user-delete', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:users-list'), follow=True),
                     client.get(reverse_lazy('users:user-update', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:group-create'), follow=True),
                     client.get(reverse_lazy('users:group-delete', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-delete-user',
                                             kwargs={'pk': self.group.pk, 'upk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:group-delete-all-users', kwargs={'pk': self.group.pk}),
                                follow=True),
                     client.get(reverse_lazy('users:group-add-users', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-info', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:groups-list'), follow=True),
                     client.get(reverse_lazy('users:group-members', kwargs={'pk': self.group.pk}), follow=True),
                     client.get(reverse_lazy('users:group-update', kwargs={'pk': self.group.pk}), follow=True)]

        for response in responses:
            self.assertNotContains(response, "You don\'t have permission to")
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    def test_permissions_group_himself(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Users Himself permissions.')

        # unauthorized
        permissions = [
            Permission.objects.get(codename='view_profile'),
            Permission.objects.get(codename='change_profile'),
            Permission.objects.get(codename='delete_profile')
        ]

        for permission in permissions:
            self.group.permissions.add(permission)

        responses = [client.get(reverse_lazy('users:user-delete', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user_test.pk}), follow=True),
                     client.get(reverse_lazy('users:user-update', kwargs={'pk': self.user_test.pk}), follow=True)]

        pattern = re.compile(r'You are not authorized to (view|modify|delete) the accounts of other users!')
        for response in responses:
            self.assertTrue(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertEqual(response.redirect_chain, [('/', 302)])

        # authorized
        responses = [client.get(reverse_lazy('users:user-delete', kwargs={'pk': self.user.pk}), follow=True),
                     client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user.pk}), follow=True),
                     client.get(reverse_lazy('users:user-update', kwargs={'pk': self.user.pk}), follow=True)]

        for response in responses:
            self.assertFalse(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    def test_permissions_group_admin(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Users Admin permissions.')

        # unauthorized
        permissions = [
            Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='delete_user'),
        ]

        for permission in permissions:
            self.group.permissions.add(permission)

        responses = [client.get(reverse_lazy('users:user-delete', kwargs={'pk': self.admin.pk}), follow=True),
                     client.get(reverse_lazy('users:user-update', kwargs={'pk': self.admin.pk}), follow=True)]

        pattern = re.compile(r'Only a superuser can (modify|delete|view) a superuser!')
        for response in responses:
            self.assertTrue(pattern.search(
                re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))
            ))
            self.assertEqual(response.redirect_chain, [('/', 302)])

    # ----------------
    # ----- User ------
    # ----------------
    def test_user_create_and_update(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='add_user'))
        self.group.permissions.add(Permission.objects.get(codename='view_user'))
        self.group.permissions.add(Permission.objects.get(codename='change_user'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserCreateView and UserUpdateView.')

        # user creation
        response = client.post(reverse_lazy('users:user-create'),
                               {
                                   'username': 'test',
                                   'email': 'test@balto.org',
                                   'phone': '1212121212',
                                   'password1': 'hello123hello123',
                                   'password2': 'hello123hello123'
                               },
                               follow=True)
        try:
            user = User.objects.get(username='test')
        except User.DoesNotExist:
            user = None
        self.assertIsNotNone(user, 'The user was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/users/{user.pk}/user-info', 302)])

        # update user
        response = client.post(reverse_lazy('users:user-update', kwargs={'pk': user.pk}),
                               {
                                   'username': user.username,
                                   'email': user.email,
                                   'phone': '2121212121',
                                   'groups': self.group.pk
                               },
                               follow=True)
        user = User.objects.get(pk=user.pk)  # retrieve updated object
        self.assertNotEqual(user.phone, '1212121212', 'The user was not updated correctly from the view.')
        self.assertEqual(user.phone, '2121212121', 'The user was not updated correctly from the view.')
        self.assertTrue(user.groups.count() == 0, 'The user was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/users/{user.pk}/user-info', 302)])

    def test_user_delete(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_user'))
        self.group.permissions.add(Permission.objects.get(codename='delete_user'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserDeleteView.')
        # delete user
        response = client.post(reverse_lazy('users:user-delete', kwargs={'pk': self.user_test.pk}), follow=True)
        self.assertRaises(User.DoesNotExist, User.objects.get, pk=self.user_test.pk)
        self.assertEqual(response.redirect_chain, [(f'/users/users-list/', 302)])

    def test_user_info(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_user'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserInfoView.')
        # info user
        response = client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user_test.pk}))
        self.assertEqual(response.context_data['object'], self.user_test, 'The user does not match.')

    def test_user_update_profile(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_profile'))
        self.group.permissions.add(Permission.objects.get(codename='change_profile'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserCreateView and UserUpdateView.')
        # update profile
        temp_group = Group.objects.create(name='temp')
        response = client.post(reverse_lazy('users:user-update', kwargs={'pk': self.user.pk}),
                               {
                                   'username': self.user.username,
                                   'email': self.user.email,
                                   'phone': '2121212121',
                                   'groups': temp_group.pk  # field non present (downgraded form, see forms.py)
                               },
                               follow=True)
        user = User.objects.get(pk=self.user.pk)  # retrieve updated object
        self.assertTrue(
            user.groups.count() == 1,  # 1 because self.user is a self.group member
            'User added himself to a group without permission.'
        )
        self.assertEqual(user.groups.all()[0], self.group, 'user.groups[0] does not match.')
        self.assertNotEqual(user.phone, '1111111111', 'The user was not updated correctly from the view.')
        self.assertEqual(user.phone, '2121212121', 'The user was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/users/{user.pk}/user-info', 302)])

    def test_user_delete_profile(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='delete_profile'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserDeleteView.')
        # delete profile
        response = client.post(reverse_lazy('users:user-delete', kwargs={'pk': self.user.pk}), follow=True)
        self.assertRaises(User.DoesNotExist, User.objects.get, pk=self.user.pk)
        self.assertEqual(response.redirect_chain, [('/users/users-list/', 302),
                                                   ('/users/login/?next=/users/users-list/', 302)])  # logged out

    def test_user_info_profile(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_profile'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserInfoView.')
        # info profile
        response = client.get(reverse_lazy('users:user-info', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.context_data['object'], self.user, 'The user does not match.')

    def test_users_list(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_user'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test UserListView.')
        # list user
        response = client.get(reverse_lazy('users:users-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], User.objects.all(),
                                 msg='The users do not match.')

    # ----------------
    # ----- Group -----
    # ----------------
    def test_group_create_and_update(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='add_group'))
        self.group.permissions.add(Permission.objects.get(codename='view_group'))
        self.group.permissions.add(Permission.objects.get(codename='change_group'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupCreateView and GroupUpdateView.')

        # group creation
        response = client.post(reverse_lazy('users:group-create'),
                               {
                                   'name': 'test',
                                   'permissions': Permission.objects.get(codename='add_animal').pk
                               },
                               follow=True)
        try:
            group = Group.objects.get(name='test')
        except Group.DoesNotExist:
            group = None
        self.assertIsNotNone(group, 'The group was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/users/{group.pk}/group-info', 302)])

        # update group
        response = client.post(reverse_lazy('users:group-update', kwargs={'pk': group.pk}),
                               {
                                   'name': group.name,
                                   'permissions': [Permission.objects.get(codename='add_animal').pk,
                                                   Permission.objects.get(codename='change_animal').pk,
                                                   Permission.objects.get(codename='delete_animal').pk,
                                                   Permission.objects.get(codename='view_animal').pk]
                               },
                               follow=True)
        group = Group.objects.get(pk=group.pk)  # retrieve updated object
        self.assertNotEqual(group.permissions.count(), 1, 'The group was not updated correctly from the view.')
        self.assertEqual(group.permissions.count(), 4, 'The group was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/users/{group.pk}/group-info', 302)])

    def test_group_delete(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_group'))
        self.group.permissions.add(Permission.objects.get(codename='delete_group'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupDeleteView.')
        # delete group (with members)
        response = client.post(reverse_lazy('users:group-delete', kwargs={'pk': self.group.pk}), follow=True)
        pattern = re.compile(r'There (are \d+ users|is a user) in this group, it cannot be deleted!')
        self.assertTrue(pattern.search(re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))))
        # delete group (without members)
        temp_group = Group.objects.create(name='temp')
        response = client.post(reverse_lazy('users:group-delete', kwargs={'pk': temp_group.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [('/users/groups-list/', 302)])
        self.assertRaises(Group.DoesNotExist, Group.objects.get, pk=temp_group.pk)

    def test_group_info(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_group'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupInfoView.')
        # info group
        response = client.get(reverse_lazy('users:group-info', kwargs={'pk': self.group.pk}))
        self.assertEqual(response.context_data['object'], self.group, 'The group does not match.')

    def test_groups_list(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='view_group'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupListView.')
        # list group
        response = client.get(reverse_lazy('users:groups-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], Group.objects.all(),
                                 msg='The groups do not match.')

    def test_group_delete_user(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='group_view_members'))
        self.group.permissions.add(Permission.objects.get(codename='group_delete_users'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupDeleteUserView.')
        # delete group member
        self.group.user_set.add(self.user_test)
        response = client.post(reverse_lazy('users:group-delete-user',
                                            kwargs={'pk': self.group.pk, 'upk': self.user_test.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/users/{self.group.pk}/group-members', 302)])
        self.assertTrue(User.objects.get(pk=self.user_test.pk).groups.count() == 0,
                        'user.groups still refers to a group')

    def test_group_delete_all_users(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='group_view_members'))
        self.group.permissions.add(Permission.objects.get(codename='group_delete_users'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupDeleteAllUsersView.')
        # delete all group members
        temp_group = Group.objects.create(name='temp')
        temp_user1 = User.objects.create_user(username='temp_user1', email='temp_user1@balto.org', phone='2222222222',
                                              password='hello123hello123')
        temp_user2 = User.objects.create_user(username='temp_user2', email='temp_user2@balto.org', phone='3333333333',
                                              password='hello123hello123')
        temp_group.user_set.add(temp_user1)
        temp_group.user_set.add(temp_user2)
        response = client.post(reverse_lazy('users:group-delete-all-users', kwargs={'pk': temp_group.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/users/{temp_group.pk}/group-members', 302)])
        self.assertTrue(User.objects.get(pk=temp_user1.pk).groups.count() == 0,
                        'temp_user1.groups still refers to a group')
        self.assertTrue(User.objects.get(pk=temp_user2.pk).groups.count() == 0,
                        'temp_user2.groups still refers to a group')

    def test_group_add_user(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='group_view_members'))
        self.group.permissions.add(Permission.objects.get(codename='group_add_users'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupAddUsersView.')
        # add user to group
        temp_group = Group.objects.create(name='temp')
        temp_user1 = User.objects.create_user(username='temp_user1', email='temp_user1@balto.org', phone='2222222222',
                                              password='hello123hello123')
        temp_user2 = User.objects.create_user(username='temp_user2', email='temp_user2@balto.org', phone='3333333333',
                                              password='hello123hello123')
        response = client.post(reverse_lazy('users:group-add-users', kwargs={'pk': temp_group.pk}),
                               {
                                   'users': [temp_user1.pk, temp_user2.pk]
                               },
                               follow=True)
        self.assertEqual(response.redirect_chain, [(f'/users/{temp_group.pk}/group-members', 302)])
        self.assertTrue(User.objects.get(pk=temp_user1.pk).groups.count() == 1,
                        'temp_user1.groups does not refer to any group.')
        self.assertTrue(User.objects.get(pk=temp_user2.pk).groups.count() == 1,
                        'temp_user2.groups does not refer to any group.')
        self.assertEqual(User.objects.get(pk=temp_user1.pk).groups.all()[0], temp_group,
                         'temp_user1.groups[0] does not match.')
        self.assertEqual(User.objects.get(pk=temp_user2.pk).groups.all()[0], temp_group,
                         'temp_user2.groups[0] does not match.')

    def test_group_members(self):
        client = Client()
        self.group.permissions.add(Permission.objects.get(codename='group_view_members'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test GroupMembersView.')
        # list group members
        self.group.user_set.add(self.user_test)
        response = client.get(reverse_lazy('users:group-members', kwargs={'pk': self.group.pk}))
        self.assertEqual(response.context_data['group'], self.group, msg='The group does not match.')
        self.assertQuerysetEqual(response.context_data['members'], self.group.user_set.all(),
                                 msg='The members do not match.')
