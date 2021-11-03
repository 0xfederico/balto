from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from Configurations.mixins import CreatedModifiedMixin


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, = cls.objects.get_or_create(pk=1, defaults={'created': timezone.now()})
        return obj


class LegalInformation(CreatedModifiedMixin, SingletonModel):
    email = models.EmailField(verbose_name='Contact email')
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',
                                                                              message='phone numbers are '
                                                                                      '10 digits long')],
                                    blank=False, verbose_name='Your mobile phone number')
    landline_phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{10}$',
                                                                                message='phone numbers are '
                                                                                        '10 digits long')],
                                      blank=False, verbose_name='Your landline phone number')
    about_us = models.TextField()
    responsible = models.CharField(max_length=50)


class Area(CreatedModifiedMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        permissions = (('area_add_boxes', 'Can add boxes to area'),
                       ('area_delete_boxes', 'Can delete boxes from area'),
                       ('area_view_boxes', 'Can view area boxes'))  # added to defaults


class Box(CreatedModifiedMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)
    located_area = models.ForeignKey(Area, related_name='composedby', on_delete=models.PROTECT, null=True)

    # this method is not implemented by default in models
    def __str__(self):
        return self.name
