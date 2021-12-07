# Generated by Django 3.2.8 on 2021-11-30 14:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('area_add_boxes', 'Can add boxes to area'), ('area_delete_boxes', 'Can delete boxes from area'), ('area_view_boxes', 'Can view area boxes')),
            },
        ),
        migrations.CreateModel(
            name='LegalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('email', models.EmailField(max_length=254, verbose_name='Contact email')),
                ('name', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('mobile_phone', models.CharField(help_text='Your mobile phone number', max_length=10, validators=[django.core.validators.RegexValidator(message='mobile phone numbers are 10 digits long', regex='^\\d{10}$')])),
                ('landline_phone', models.CharField(help_text='Your landline phone number', max_length=9, validators=[django.core.validators.RegexValidator(message='landline phone numbers are 9 digits long', regex='^\\d{9}$')])),
                ('about_us', models.TextField()),
                ('responsible', models.CharField(max_length=50)),
            ],
            options={
                'default_permissions': ('change', 'view'),
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=50, unique=True)),
                ('located_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='composedby', to='facility.area')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]