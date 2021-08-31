from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


def user_directory_path(instance, filename):
    return f'users_{instance.user.id}' / date.today() / filename


class UserModel(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) #DOC: Set this flag to False instead of deleting accounts
    phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$', message="phone numbers are 10 digits long")], blank=False, unique=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='User photo', blank=True, null=True)

    class Meta:
        verbose_name = 'Generic User'
        verbose_name_plural = 'Users'
        ordering = ['last_name']


# voluntary = Group.objects.create(name='Voluntary')
# educator = Group.objects.create(name='Educator')
# distance_adopter = Group.objects.create(name='DistanceAdopter')

