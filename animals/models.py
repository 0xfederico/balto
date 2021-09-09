from django.core.validators import RegexValidator
from django.db import models
from datetime import date


def animal_directory_path(self, filename):
    return f"animals_{self.pk}_{date.today()}_{filename}"


class AnimalModel(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    breed = models.CharField(max_length=30)
    sex = models.CharField(max_length=10)
    microchip = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{15}$',
                                 message="the microchip code is 15 numbers long")],
                                 blank=False, unique=True, verbose_name="The code of the animal's microchip")
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
    photo = models.ImageField(upload_to=animal_directory_path, verbose_name='Choose the profile picture of the animal',
                              blank=True)

    class Meta:
        ordering = ['name']
        permissions = (("animal.prepare_food", "Can prepare food for animals"),
                       ("animal.give_food", "Can give food to animals"),
                       ("animal.give_medicine", "Can give medicine to animals"),
                       ("animal.go_for_a_walk", "Can go for a walk with animals"),
                       ("animal.put_in_the_walking_area", "Can put animals in the walking area "))  # added to defaults
