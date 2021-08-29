from django.db import models
from datetime import date


def animals_directory_path(instance, filename):
    return f'animal_{instance.user.id}' / date.today() / filename


class Animal(models.Model):
    name = models.CharField(max_length=30)
    breed = models.CharField(max_length=30)
    sex = models.CharField(max_length=10)
    microchip = models.CharField(max_length=15)
    particular_signs = models.TextField()
    check_in_date = models.DateField()
    birth_date = models.DateField()
    sociability_with_females = models.BooleanField()
    sociability_with_males = models.BooleanField()
    sociability_with_children = models.BooleanField()
    needs_another_dog = models.BooleanField()
    needs_garden = models.BooleanField()
    pathologies = models.CharField(max_length=100)
    walk_equipment = models.CharField(max_length=20)
    photo = models.ImageField(upload_to=animals_directory_path, verbose_name='User photo', blank=True)

    class Meta:
        verbose_name_plural = 'Animals'

