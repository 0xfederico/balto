from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from Configurations.mixins import CreatedModifiedMixin


def user_directory_path(self, filename):
    return f"users_{self.pk}_{date.today()}_{filename}"


class User(AbstractUser, CreatedModifiedMixin):
    email = models.EmailField(blank=False, unique=True, verbose_name="Your email")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # DOC: Set this flag to False instead of deleting accounts
    phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',
                                                                       message="phone numbers are 10 digits long")],
                             blank=False, unique=True, verbose_name="Your phone number")
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Choose your profile picture', blank=True,
                              null=True)

    class Meta:
        ordering = ['username']
        permissions = (("group.add_users_to_group", "Can add users to group"),
                       ("group.delete_users_from_group", "Can delete users from group"),
                       ("group.view_members", "Can view group members"),
                       ("view_profile", "Can view his own profile"),
                       ("change_profile", "Can change his own profile"),
                       ("delete_profile", "Can delete his own profile"))  # added to defaults
