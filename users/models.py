from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from Configurations.mixins import CreatedModifiedMixin


def user_directory_path(self, filename):
    return f'users_{self.pk}_{date.today()}_{filename}'


class User(AbstractUser, CreatedModifiedMixin):
    email = models.EmailField(blank=False, unique=True, help_text='Your email')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # DOC: Set this flag to False instead of deleting accounts
    phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',
                                                                       message='phone numbers are 10 digits long')],
                             blank=False, unique=True, help_text='Your phone number')
    photo = models.ImageField(upload_to=user_directory_path, help_text='Choose your profile picture', blank=True,
                              null=True)

    class Meta:
        ordering = ['username']
        permissions = (('group_add_users', 'Can add members to group'),
                       ('group_delete_users', 'Can delete members from group'),
                       ('group_view_members', 'Can view group members'),
                       ('view_profile', 'Can view his own profile'),
                       ('change_profile', 'Can change his own profile'),
                       ('delete_profile', 'Can delete his own profile'))  # added to defaults
