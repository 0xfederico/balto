from django.db.models import ProtectedError
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import re
import os
import django

# without this setup it is not possible to import the app models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configurations.settings')
django.setup()

from animals.models import Animal, AnimalHealth, AnimalManagement, AnimalDescription
from facility.models import Area, Box
from django.contrib.auth.models import Permission
from users.models import User


class ArchitecturalConsistencyTests(TestCase):
    def setUp(self):
        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing boxes
        for box in Box.objects.all():
            box.delete()

        # delete all existing areas
        for area in Area.objects.all():
            area.delete()

        # areas, box, animals creation
        self.area = Area.objects.create(name='testarea')
        self.box = Box.objects.create(name='testbox', located_area=self.area)
        animal_health = AnimalHealth.objects.create(pathologies='none', diet='complete', note='none')
        animal_management = AnimalManagement.objects.create(sociability_with_females=True,
                                                            sociability_with_males=False,
                                                            sociability_with_children=True,
                                                            needs_another_dog=False, needs_garden=True,
                                                            walk_equipment='harness', flag_warning='yellow')
        animal_description = AnimalDescription.objects.create(size='67cm', color='black', spots='none',
                                                              ears='triangular, erected', hair_length='20cm',
                                                              tail='40cm long and bushy', origin='none',
                                                              particular_signs='none')
        self.animal = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                            check_in_date=timezone.now().date() - timedelta(days=20),
                                            birth_date=timezone.now().date() - timedelta(days=365), box=self.box,
                                            health=animal_health, management=animal_management,
                                            description=animal_description)

    def test_objects_are_instances_of_the_expected_class(self):
        self.assertTrue(isinstance(self.box.located_area, Area), 'box.located_area is not an instance of Area.')
        self.assertTrue(isinstance(self.animal.box, Box), 'animal.box is not an instance of Box.')
        self.assertTrue(isinstance(self.animal.health, AnimalHealth),
                        'animal.health is not an instance of AnimalHealth.')
        self.assertTrue(isinstance(self.animal.management, AnimalManagement),
                        'animal.management is not an instance of AnimalManagement.')
        self.assertTrue(isinstance(self.animal.description, AnimalDescription),
                        'animal.description is not an instance of AnimalDescription.')

    def test_cancellation_of_animal_related_models(self):
        health = management = description = None
        try:
            health = AnimalHealth.objects.get(pk=self.animal.health.pk)
            management = AnimalManagement.objects.get(pk=self.animal.management.pk)
            description = AnimalDescription.objects.get(pk=self.animal.description.pk)
        except (AnimalHealth.DoesNotExist, AnimalManagement.DoesNotExist, AnimalDescription.DoesNotExist):
            pass
        self.assertIsNotNone(health)
        self.assertIsNotNone(management)
        self.assertIsNotNone(description)

        self.assertRaises(ProtectedError, self.animal.health.delete)
        self.assertRaises(ProtectedError, self.animal.management.delete)
        self.assertRaises(ProtectedError, self.animal.description.delete)

        self.animal.delete()

        self.assertRaises(AnimalHealth.DoesNotExist, AnimalHealth.objects.get, pk=self.animal.health.pk)
        self.assertRaises(AnimalManagement.DoesNotExist, AnimalManagement.objects.get, pk=self.animal.management.pk)
        self.assertRaises(AnimalDescription.DoesNotExist, AnimalDescription.objects.get, pk=self.animal.description.pk)


# You may need to add 'testserver' to ALLOWED_HOSTS.
from Configurations.settings import ALLOWED_HOSTS
ALLOWED_HOSTS.append('testserver')


class ViewsTests(TestCase):
    def setUp(self):
        # delete all existing animals
        for animal in Animal.objects.all():
            animal.delete()

        # delete all existing boxes
        for box in Box.objects.all():
            box.delete()

        # delete all existing areas
        for area in Area.objects.all():
            area.delete()

        # delete all existing users
        for user in User.objects.all():
            user.delete()

        # user creation
        self.user = User.objects.create_user(username='user', email='user@balto.org', phone='1111111111',
                                             password='hello123hello123')

        # areas, box, animals creation
        self.area = Area.objects.create(name='testarea')
        self.box = Box.objects.create(name='testbox', located_area=self.area)
        animal_health = AnimalHealth.objects.create(pathologies='none', diet='complete', note='none')
        animal_management = AnimalManagement.objects.create(sociability_with_females=True,
                                                            sociability_with_males=False,
                                                            sociability_with_children=True,
                                                            needs_another_dog=False, needs_garden=True,
                                                            walk_equipment='harness', flag_warning='yellow')
        animal_description = AnimalDescription.objects.create(size='67cm', color='black', spots='none',
                                                              ears='triangular, erected', hair_length='20cm',
                                                              tail='40cm long and bushy', origin='none',
                                                              particular_signs='none')
        self.animal = Animal.objects.create(name='Rex', breed='German Shepard', sex='Male', microchip=111111111111111,
                                            check_in_date=timezone.now().date() - timedelta(days=20),
                                            birth_date=timezone.now().date() - timedelta(days=365), box=self.box,
                                            health=animal_health, management=animal_management,
                                            description=animal_description)

    # ---------------
    # - Permissions -
    # ---------------
    def test_permissions(self):
        client = Client()
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test Animals permissions.')

        responses = [client.get(reverse_lazy('animals:animal-create'), follow=True),
                     client.get(reverse_lazy('animals:animal-delete', kwargs={'pk': self.animal.pk}), follow=True),
                     client.get(reverse_lazy('animals:animal-info', kwargs={'pk': self.animal.pk}), follow=True),
                     client.get(reverse_lazy('animals:animals-list'), follow=True),
                     client.get(reverse_lazy('animals:animal-update', kwargs={'pk': self.animal.pk}), follow=True)]

        for response in responses:
            self.assertContains(response, "You don\'t have permission to")
            self.assertEqual(response.redirect_chain, [('/', 302)])

        self.user.user_permissions.add(Permission.objects.get(codename='add_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_animal'))

        pattern_health = re.compile(r'<h3.*>.*Health.*</h3>')
        pattern_management = re.compile(r'<h3.*>.*Management.*</h3>')
        pattern_description = re.compile(r'<h3.*>.*Description.*</h3>')

        response_create = client.get(reverse_lazy('animals:animal-create'))
        response_update = client.get(reverse_lazy('animals:animal-update', kwargs={'pk': self.animal.pk}))
        response_create_decoded = re.sub(' +', ' ', response_create.content.decode('utf-8').strip().replace('\n', ''))
        response_update_decoded = re.sub(' +', ' ', response_update.content.decode('utf-8').strip().replace('\n', ''))
        self.assertFalse(pattern_health.search(response_create_decoded))
        self.assertFalse(pattern_management.search(response_create_decoded))
        self.assertFalse(pattern_description.search(response_create_decoded))
        self.assertFalse(pattern_health.search(response_update_decoded))
        self.assertFalse(pattern_management.search(response_update_decoded))
        self.assertFalse(pattern_description.search(response_update_decoded))

        permissions = [Permission.objects.get(codename='add_animalhealth'),
                       Permission.objects.get(codename='add_animalmanagement'),
                       Permission.objects.get(codename='add_animaldescription'),
                       Permission.objects.get(codename='change_animalhealth'),
                       Permission.objects.get(codename='change_animalmanagement'),
                       Permission.objects.get(codename='change_animaldescription')]
        for permission in permissions:
            self.user.user_permissions.add(permission)

        response_create = client.get(reverse_lazy('animals:animal-create'))
        response_update = client.get(reverse_lazy('animals:animal-update', kwargs={'pk': self.animal.pk}))
        response_create_decoded = re.sub(' +', ' ', response_create.content.decode('utf-8').strip().replace('\n', ''))
        response_update_decoded = re.sub(' +', ' ', response_update.content.decode('utf-8').strip().replace('\n', ''))
        self.assertTrue(pattern_health.search(response_create_decoded))
        self.assertTrue(pattern_management.search(response_create_decoded))
        self.assertTrue(pattern_description.search(response_create_decoded))
        self.assertTrue(pattern_health.search(response_update_decoded))
        self.assertTrue(pattern_management.search(response_update_decoded))
        self.assertTrue(pattern_description.search(response_update_decoded))

        self.user.user_permissions.add(Permission.objects.get(codename='delete_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_animal'))

        responses = [client.get(reverse_lazy('animals:animal-create'), follow=True),
                     client.get(reverse_lazy('animals:animal-delete', kwargs={'pk': self.animal.pk}), follow=True),
                     client.get(reverse_lazy('animals:animal-info', kwargs={'pk': self.animal.pk}), follow=True),
                     client.get(reverse_lazy('animals:animals-list'), follow=True),
                     client.get(reverse_lazy('animals:animal-update', kwargs={'pk': self.animal.pk}), follow=True)]

        for response in responses:
            self.assertNotContains(response, "You don\'t have permission to")
            self.assertNotEqual(response.redirect_chain, [('/', 302)])

    # ---------------
    # --- Animals ---
    # ---------------
    def test_animal_create_and_update(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='add_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_animalhealth'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_animalmanagement'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_animaldescription'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_animalhealth'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_animalmanagement'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_animaldescription'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AnimalCreateView and AnimalUpdateView.')

        # animal creation
        response = client.post(reverse_lazy('animals:animal-create'),
                               {
                                   'name': 'Lassie',
                                   'breed': 'Rough Collie',
                                   'sex': 'Female',
                                   'microchip': 222222222222222,
                                   'check_in_date': timezone.now().date() - timedelta(days=20),
                                   'birth_date': timezone.now().date() - timedelta(days=182),
                                   'box': self.box.pk,
                                   'diet': 'complete',
                                   'sociability_with_males': True,
                                   'walk_equipment': 'harness',
                                   'flag_warning': 'yellow',
                                   'particular_signs': 'none'
                               },
                               follow=True)
        try:
            animal = Animal.objects.get(name='Lassie')
        except Animal.DoesNotExist:
            animal = None
        self.assertIsNotNone(animal, 'The animal was not created correctly from the view.')
        self.assertIsNotNone(animal.health, 'The animal was not created correctly from the view.')
        self.assertIsNotNone(animal.management, 'The animal was not created correctly from the view.')
        self.assertIsNotNone(animal.description, 'The animal was not created correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/animals/{animal.pk}/animal-info', 302)])

        # update animal
        new_box = Box.objects.create(name='new box', located_area=self.area)
        response = client.post(reverse_lazy('animals:animal-update', kwargs={'pk': animal.pk}),
                               {
                                   'name': animal.name,
                                   'breed': animal.breed,
                                   'sex': animal.sex,
                                   'microchip': 123456789012345,
                                   'check_in_date': animal.check_in_date,
                                   'birth_date': animal.birth_date,
                                   'box': new_box.pk,
                                   'diet': animal.health.diet,
                                   'sociability_with_females': animal.management.sociability_with_females,
                                   'sociability_with_males': animal.management.sociability_with_males,
                                   'walk_equipment': animal.management.walk_equipment,
                                   'flag_warning': animal.management.flag_warning,
                                   'particular_signs': animal.description.particular_signs
                               },
                               follow=True)
        animal = Animal.objects.get(pk=animal.pk)  # retrieve updated object
        self.assertNotEqual(animal.microchip, '222222222222222', 'The animal was not updated correctly from the view.')
        self.assertNotEqual(animal.box.pk, self.box.pk, 'The animal was not updated correctly from the view.')
        self.assertEqual(animal.microchip, '123456789012345', 'The animal was not updated correctly from the view.')
        self.assertEqual(animal.box.pk, new_box.pk, 'The animal was not updated correctly from the view.')
        self.assertEqual(response.redirect_chain, [(f'/animals/{animal.pk}/animal-info', 302)])

    def test_animal_delete(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_animal'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AnimalDeleteView.')
        # delete animal
        response = client.post(reverse_lazy('animals:animal-delete', kwargs={'pk': self.animal.pk}), follow=True)
        self.assertEqual(response.redirect_chain, [(f'/animals/animals-list/', 302)])
        self.assertRaises(Animal.DoesNotExist, Animal.objects.get, pk=self.animal.pk)
        self.assertRaises(AnimalHealth.DoesNotExist, AnimalHealth.objects.get, pk=self.animal.health.pk)
        self.assertRaises(AnimalManagement.DoesNotExist, AnimalManagement.objects.get, pk=self.animal.management.pk)
        self.assertRaises(AnimalDescription.DoesNotExist, AnimalDescription.objects.get, pk=self.animal.description.pk)

    def test_animal_info(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_animal'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_animalhealth'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_animalmanagement'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_animaldescription'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AnimalInfoView.')
        # info animal
        response = client.get(reverse_lazy('animals:animal-info', kwargs={'pk': self.animal.pk}))
        self.assertEqual(response.context_data['object'], self.animal, 'The animal does not match.')
        self.assertEqual(response.context_data['health'], self.animal.health, 'The animal health does not match.')
        self.assertEqual(response.context_data['management'], self.animal.management,
                         'The animal management does not match.')
        self.assertEqual(response.context_data['description'], self.animal.description,
                         'The animal description does not match.')

    def test_animals_list(self):
        client = Client()
        self.user.user_permissions.add(Permission.objects.get(codename='view_animal'))
        self.assertTrue(client.login(username='user', password='hello123hello123'),
                        'The user cannot log in to test AnimalListView.')
        # list animal
        response = client.get(reverse_lazy('animals:animals-list'))
        self.assertQuerysetEqual(response.context_data['object_list'], Animal.objects.all(),
                                 msg='The animals do not match.')
