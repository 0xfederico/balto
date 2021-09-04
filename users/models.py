from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from Configurations.settings import BASE_DIR


def user_directory_path(instance, filename):
    return BASE_DIR / f'users_{instance.user.id}' / date.today() / filename


class UserModel(AbstractUser):

    email = models.EmailField(blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # DOC: Set this flag to False instead of deleting accounts
    phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',
                             message="phone numbers are 10 digits long")], blank=False, unique=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='User photo', blank=True, null=True)
    is_responsible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Generic User'
        verbose_name_plural = 'Users'
        ordering = ['last_name']
