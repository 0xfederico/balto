from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import os
import re
import django

# without this setup it is not possible to import the app models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configurations.settings')
django.setup()

from django.contrib.auth.models import Permission
from animals.models import Animal
from facility.models import Area, Box, LegalInformation
from users.models import User


class ArchitecturalConsistencyTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing boxes
        for box in Box.objects.all():
            box.delete()

        # delete all existing areas
        for area in Area.objects.all():
            area.delete()

        # delete all existing legalinformations
        for legalinfo in LegalInformation.objects.all():
            legalinfo.delete()

        # areas, box, animals creation
        self.area1 = Area.objects.create(name='testarea1')
        self.area2 = Area.objects.create(name='testarea2')
        self.box1 = Box.objects.create(name='testbox1', located_area=self.area1)
        self.box2 = Box.objects.create(name='testbox2', located_area=self.area1)
        self.animal1 = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=365), box=self.box1)
        self.animal2 = Animal.objects.create(name='Lassie', breed='Rough Collie', sex='Female',
                                             microchip=222222222222222,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=182), box=self.box1)

        # legalinformation creation
        self.legalinfo = LegalInformation.objects.create(email='admin@balto.org', name='Balto s.r.l',
                                                         region='Calabria', city='Mormanno', province='Cosenza',
                                                         address="Via Sant'Anna", mobile_phone='1111111111',
                                                         landline_phone='111111111', about_us='Lorem Ipsum',
                                                         responsible='Giuseppe')

    def test_objects_are_instances_of_the_expected_class(self):
        self.assertTrue(isinstance(self.box1.located_area, Area), 'box1.located_area is not an instance of Area.')
        self.assertTrue(isinstance(self.box2.located_area, Area), 'box2.located_area is not an instance of Area.')
        self.assertTrue(isinstance(self.animal1.box, Box), 'animal1.box is not an instance of Box.')
        self.assertTrue(isinstance(self.animal2.box, Box), 'animal2.box is not an instance of Box.')

    def test_legalinformation_singleton(self):
        self.assertRaises(IntegrityError, LegalInformation.objects.create, email='test@balto.org', name='Test s.r.l',
                          region='test', city='test', province='test', address="test", mobile_phone='2222222222',
                          landline_phone='111111111', about_us='test', responsible='Test')


# You may need to add 'testserver' to ALLOWED_HOSTS.
from Configurations.settings import ALLOWED_HOSTS
ALLOWED_HOSTS.append('testserver')


class ViewsTests(TestCase):
    def setUp(self):
        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing boxes
        for box in Box.objects.all():
            box.delete()

        # delete all existing areas
        for area in Area.objects.all():
            area.delete()

        # delete all existing legalinformations
        for legalinfo in LegalInformation.objects.all():
            legalinfo.delete()

        # user creation
        self.user = User.objects.create_user(username='user', email='user@balto.org', phone='1111111111',
                                             password='hello123hello123')

        # areas, box, animals creation
        self.area1 = Area.objects.create(name='testarea1')
        self.area2 = Area.objects.create(name='testarea2')
        self.box1 = Box.objects.create(name='testbox1', located_area=self.area1)
        self.box2 = Box.objects.create(name='testbox2', located_area=self.area1)
        self.animal1 = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=365), box=self.box1)
        self.animal2 = Animal.objects.create(name='Lassie', breed='Rough Collie', sex='Female',
                                             microchip=222222222222222,
                                             check_in_date=timezone.now().date() - timedelta(days=20),
                                             birth_date=timezone.now().date() - timedelta(days=182), box=self.box1)

    # ---------------
    # - Permissions -
    # ---------------
    def test_permissions(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Facility permissions.')

        responses = [client.get(reverse_lazy('facility:legalinformation-info'), follow=True),
                     client.get(reverse_lazy('facility:legalinformation-update'), follow=True),
                     client.get(reverse_lazy('facility:area-create'), follow=True),
                     client.get(reverse_lazy('facility:area-delete', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-delete-box',
                                             kwargs={'pk': self.area1.pk, 'bpk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-delete-all-boxes',
                                             kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-add-boxes', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-info', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:areas-list'), follow=True),
                     client.get(reverse_lazy('facility:area-boxes', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-update', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:box-create'), follow=True),
                     client.get(reverse_lazy('facility:box-delete', kwargs={'pk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:box-info', kwargs={'pk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:boxes-list'), follow=True),
                     client.get(reverse_lazy('facility:box-update', kwargs={'pk': self.box1.pk}), follow=True)]

        for response in responses:
            self.assertContains(response, "You don\'t have permission to")
            self.assertEqual(response.redirect_chain, [('/', 302)])

        permissions = [Permission.objects.get(codename='add_box'),
                       Permission.objects.get(codename='delete_box'),
                       Permission.objects.get(codename='view_box'),
                       Permission.objects.get(codename='change_box'),
                       Permission.objects.get(codename='add_area'),
                       Permission.objects.get(codename='delete_area'),
                       Permission.objects.get(codename='view_area'),
                       Permission.objects.get(codename='change_area'),
                       Permission.objects.get(codename='area_add_boxes'),
                       Permission.objects.get(codename='area_delete_boxes'),
                       Permission.objects.get(codename='area_view_boxes'),
                       Permission.objects.get(codename='view_legalinformation'),
                       Permission.objects.get(codename='change_legalinformation')]

        for permission in permissions:
            self.user.user_permissions.add(permission)

        responses = [client.get(reverse_lazy('facility:legalinformation-info'), follow=True),
                     client.get(reverse_lazy('facility:legalinformation-update'), follow=True),
                     client.get(reverse_lazy('facility:area-create'), follow=True),
                     client.get(reverse_lazy('facility:area-delete', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-delete-box',
                                             kwargs={'pk': self.area1.pk, 'bpk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-delete-all-boxes',
                                             kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-add-boxes', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-info', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:areas-list'), follow=True),
                     client.get(reverse_lazy('facility:area-boxes', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:area-update', kwargs={'pk': self.area1.pk}), follow=True),
                     client.get(reverse_lazy('facility:box-create'), follow=True),
                     client.get(reverse_lazy('facility:box-delete', kwargs={'pk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:box-info', kwargs={'pk': self.box1.pk}), follow=True),
                     client.get(reverse_lazy('facility:boxes-list'), follow=True),
                     client.get(reverse_lazy('facility:box-update', kwargs={'pk': self.box1.pk}), follow=True)]

        for response in responses:
            self.assertNotContains(response, "You don\'t have permission to")
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    # ----------------
    # ----- Box ------
    # ----------------
    def test_box_create_and_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_box'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_box'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_box'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test BoxCreateView and BoxUpdateView.')

        # box creation
        response = client.post(reverse_lazy('facility:box-create'),
                               {
                                   'name': 'test',
                                   'located_area': self.area1.pk
                               },
                               follow=True)
        try:
            box = Box.objects.get(name='test')
        except Box.DoesNotExist:
            box = None
        self.assertIsNotNone(box, 'The box was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/facility/{box.pk}/box-info', 302)])

        # update box
        response = client.post(reverse_lazy('facility:box-update', kwargs={'pk': box.pk}),
                               {
                                   'name': box.name,
                                   'located_area': self.area2.pk
                               },
                               follow=True)
        box = Box.objects.get(pk=box.pk)  # retrieve updated object
        self.assertNotEqual(box.located_area.pk, self.area1.pk, 'The box was not updated correctly from the view.')
        self.assertEqual(box.located_area.pk, self.area2.pk, 'The box was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/facility/{box.pk}/box-info', 302)])

    def test_box_delete(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_box'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_box'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test BoxDeleteView.')
        # delete box (with animal inside)
        response = client.post(reverse_lazy('facility:box-delete', kwargs={'pk': self.box1.pk}), follow=True)
        pattern = re.compile(r'There (are \d+ animals|is an animal) in this box, it cannot be deleted!')
        self.assertTrue(pattern.search(re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))))
        # delete box (without animal inside)
        response = client.post(reverse_lazy('facility:box-delete', kwargs={'pk': self.box2.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/facility/boxes-list/', 302)])
        self.assertRaises(Box.DoesNotExist, Box.objects.get, pk=self.box2.pk)

    def test_box_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_box'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test BoxInfoView.')
        # info box
        response = client.get(reverse_lazy('facility:box-info', kwargs={'pk': self.box1.pk}))
        self.assertEqual(response.context_data['object'], self.box1, 'The box does not match.')

    def test_boxes_list(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_box'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test BoxListView.')
        # list box
        response = client.get(reverse_lazy('facility:boxes-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], Box.objects.all(), msg='The boxes do not match.')

    # ----------------
    # -- LegalInfo ---
    # ----------------
    def test_legalinfo_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_legalinformation'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test LegalInformationInfoView.')
        # info legalinfo
        response = client.get(reverse_lazy('facility:legalinformation-info'))
        self.assertEqual(LegalInformation.objects.count(), 1)
        legalinfo = LegalInformation.objects.all()[0]
        self.assertEqual(response.context_data['object'], legalinfo, 'The legalinfo does not match.')

    def test_legalinfo_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_legalinformation'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_legalinformation'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test LegalInformationInfoView.')
        # update legalinfo
        response = client.post(reverse_lazy('facility:legalinformation-update'),
                               {
                                   'email': 'admin@balto.org',
                                   'name': 'Balto s.r.l',
                                   'region': 'Calabria',
                                   'city': 'Mormanno',
                                   'province': 'Cosenza',
                                   'address': "Via Sant'Anna",
                                   'mobile_phone': '1111111111',
                                   'landline_phone': '111111111',
                                   'about_us': 'Lorem Ipsum',
                                   'responsible': 'Giuseppe'
                               },
                               follow=True)
        legalinfo = LegalInformation.objects.get(pk=1)  # retrieve updated object
        self.assertEqual(legalinfo.email, 'admin@balto.org', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.name, 'Balto s.r.l', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.region, 'Calabria', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.city, 'Mormanno', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.province, 'Cosenza', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.address, "Via Sant'Anna", 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.mobile_phone, '1111111111', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.landline_phone, '111111111',
                         'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.about_us, 'Lorem Ipsum', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(legalinfo.responsible, 'Giuseppe', 'The legalinfo was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/facility/legalinformation-info', 302)])

    # ----------------
    # ----- Area -----
    # ----------------
    def test_area_create_and_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_area'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_area'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_area'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaCreateView and AreaUpdateView.')

        # area creation
        response = client.post(reverse_lazy('facility:area-create'),
                               {
                                   'name': 'test',
                               },
                               follow=True)
        try:
            area = Area.objects.get(name='test')
        except Area.DoesNotExist:
            area = None
        self.assertIsNotNone(area, 'The area was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/facility/{area.pk}/area-info', 302)])

        # update area
        response = client.post(reverse_lazy('facility:area-update', kwargs={'pk': area.pk}),
                               {
                                   'name': 'test2',
                               },
                               follow=True)
        area = Area.objects.get(pk=area.pk)  # retrieve updated object
        self.assertNotEqual(area.name, 'test', 'The area was not updated correctly from the view.')
        self.assertEqual(area.name, 'test2', 'The area was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/facility/{area.pk}/area-info', 302)])

    def test_area_delete(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_area'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_area'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaDeleteView.')
        # delete area (with box inside)
        response = client.post(reverse_lazy('facility:area-delete', kwargs={'pk': self.area1.pk}), follow=True)
        pattern = re.compile(r'There (are \d+ boxes|is a box) in this area, it cannot be deleted!')
        self.assertTrue(pattern.search(re.sub(' +', ' ', response.content.decode('utf-8').strip().replace('\n', ''))))
        # delete area (without box inside)
        response = client.post(reverse_lazy('facility:area-delete', kwargs={'pk': self.area2.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/facility/areas-list/', 302)])
        self.assertRaises(Area.DoesNotExist, Area.objects.get, pk=self.area2.pk)

    def test_area_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_area'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaInfoView.')
        # info area
        response = client.get(reverse_lazy('facility:area-info', kwargs={'pk': self.area1.pk}))
        self.assertEqual(response.context_data['object'], self.area1, 'The area does not match.')

    def test_areas_list(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_area'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaListView.')
        # list area
        response = client.get(reverse_lazy('facility:areas-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], Area.objects.all(),
                                 msg='The areas do not match.')

    def test_area_delete_box(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='area_view_boxes'))
        self.user.user_permissions.add(Permission.objects.get(codename='area_delete_boxes'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaDeleteBoxView.')
        # delete box from area
        response = client.post(reverse_lazy('facility:area-delete-box',
                                            kwargs={'pk': self.area1.pk, 'bpk': self.box2.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/facility/{self.area1.pk}/area-boxes', 302)])
        self.assertIsNone(Box.objects.get(pk=self.box2.pk).located_area, 'box2.located_area still refers to an area')

    def test_area_delete_all_boxes(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='area_view_boxes'))
        self.user.user_permissions.add(Permission.objects.get(codename='area_delete_boxes'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaDeleteAllBoxesView.')
        # delete all box from area
        response = client.post(reverse_lazy('facility:area-delete-all-boxes',
                                            kwargs={'pk': self.area1.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/facility/{self.area1.pk}/area-boxes', 302)])
        self.assertIsNone(Box.objects.get(pk=self.box2.pk).located_area, 'box2.located_area still refers to an area')
        self.assertIsNone(Box.objects.get(pk=self.box1.pk).located_area, 'box1.located_area still refers to an area')

    def test_area_add_box(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='area_view_boxes'))
        self.user.user_permissions.add(Permission.objects.get(codename='area_add_boxes'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaAddBoxesView.')
        # add box to area
        self.box1.located_area = self.box2.located_area = None
        self.box1.save()
        self.box2.save()
        response = client.post(reverse_lazy('facility:area-add-boxes', kwargs={'pk': self.area2.pk}),
                               {
                                   'boxes': [self.box1.pk, self.box2.pk]
                               },
                               follow=True)
        self.assertEqual(response.redirect_chain, [(f'/facility/{self.area2.pk}/area-boxes', 302)])
        self.assertIsNotNone(Box.objects.get(pk=self.box2.pk).located_area,
                             'box2.located_area does not refer to any area')
        self.assertIsNotNone(Box.objects.get(pk=self.box1.pk).located_area,
                             'box1.located_area does not refer to any area')

    def test_area_boxes(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='area_view_boxes'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AreaBoxesView.')
        # list area
        response = client.get(reverse_lazy('facility:area-boxes', kwargs={'pk': self.area1.pk}))
        self.assertEqual(response.context_data['area'], self.area1, msg='The area does not match.')
        self.assertQuerysetEqual(response.context_data['boxes'], self.area1.composedby.all(),
                                 msg='The boxes do not match.')
