from datetime import date

from django.core.validators import RegexValidator
from django.db import models

from Configurations.mixins import CreatedModifiedMixin
from facility.models import Box


def animal_directory_path(self, filename):
    return f'animals_{self.pk}_{date.today()}_{filename}'


class AnimalDescription(models.Model):
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=20, blank=True)
    spots = models.CharField(max_length=20, blank=True)
    ears = models.CharField(max_length=40, blank=True)
    hair_length = models.CharField(max_length=20, blank=True)
    tail = models.CharField(max_length=40, blank=True)
    origin = models.CharField(max_length=40, blank=True)
    particular_signs = models.TextField(blank=True)

    class Meta:
        default_permissions = ('add', 'change', 'view')  # remove delete permissions for this model (unused)


class AnimalHealth(models.Model):
    pathologies = models.CharField(max_length=255, blank=True)
    diet = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        default_permissions = ('add', 'change', 'view')  # remove delete permissions for this model (unused)


class AnimalManagement(models.Model):
    sociability_with_females = models.BooleanField(blank=True)
    sociability_with_males = models.BooleanField(blank=True)
    sociability_with_children = models.BooleanField(blank=True)
    needs_another_dog = models.BooleanField(blank=True)
    needs_garden = models.BooleanField(blank=True)
    walk_equipment = models.CharField(max_length=255, blank=True)
    FLAG_WARNING_CHOICES = (
        ('green', 'Green',),
        ('yellow', 'Yellow',),
        ('orange', 'Orange',),
        ('red', 'Red',),
        ('black', 'Black',),
    )
    flag_warning = models.CharField(max_length=15, choices=FLAG_WARNING_CHOICES, blank=True)

    class Meta:
        default_permissions = ('add', 'change', 'view')  # remove delete permissions for this model (unused)


class Animal(CreatedModifiedMixin, models.Model):
    name = models.CharField(max_length=30, unique=True)
    breed = models.CharField(max_length=30)
    SEX_CHOICES = (
        ('Female', 'Female',),
        ('Male', 'Male',),
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    microchip = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{15}$',
                                                                           message='the microchip code is 15 numbers '
                                                                                   'long')],
                                 unique=True, verbose_name='Microchip code', help_text='15 numbers')
    check_in_date = models.DateField()
    birth_date = models.DateField()
    photo = models.ImageField(upload_to=animal_directory_path, help_text='Choose the profile picture of the animal',
                              blank=True)
    description = models.OneToOneField(AnimalDescription, related_name='animal', on_delete=models.PROTECT, blank=True,
                                       null=True)
    management = models.OneToOneField(AnimalManagement, related_name='animal', on_delete=models.PROTECT, blank=True,
                                      null=True)
    health = models.OneToOneField(AnimalHealth, related_name='animal', on_delete=models.PROTECT, blank=True, null=True)
    box = models.ForeignKey(Box, related_name='who_lives_here', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['name']

    # this method is not implemented by default in models
    def __str__(self):
        return self.name

    # when an animal is deleted, a cascade is applied to the three connected tables
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.description:
            self.description.delete()
        if self.management:
            self.management.delete()
        if self.health:
            self.health.delete()
