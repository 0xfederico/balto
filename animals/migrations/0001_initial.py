# Generated by Django 3.2.8 on 2021-11-30 14:34

import animals.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=20)),
                ('color', models.CharField(blank=True, max_length=20)),
                ('spots', models.CharField(blank=True, max_length=20)),
                ('ears', models.CharField(blank=True, max_length=40)),
                ('hair_length', models.CharField(blank=True, max_length=20)),
                ('tail', models.CharField(blank=True, max_length=40)),
                ('origin', models.CharField(blank=True, max_length=40)),
                ('particular_signs', models.TextField(blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'view'),
            },
        ),
        migrations.CreateModel(
            name='AnimalHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pathologies', models.CharField(blank=True, max_length=255)),
                ('diet', models.CharField(blank=True, max_length=255)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'default_permissions': ('add', 'change', 'view'),
            },
        ),
        migrations.CreateModel(
            name='AnimalManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sociability_with_females', models.BooleanField(blank=True)),
                ('sociability_with_males', models.BooleanField(blank=True)),
                ('sociability_with_children', models.BooleanField(blank=True)),
                ('needs_another_dog', models.BooleanField(blank=True)),
                ('needs_garden', models.BooleanField(blank=True)),
                ('walk_equipment', models.CharField(blank=True, max_length=255)),
                ('flag_warning', models.CharField(blank=True, choices=[('green', 'Green'), ('yellow', 'Yellow'), ('orange', 'Orange'), ('red', 'Red'), ('black', 'Black')], max_length=15)),
            ],
            options={
                'default_permissions': ('add', 'change', 'view'),
            },
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=30, unique=True)),
                ('breed', models.CharField(max_length=30)),
                ('sex', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=6)),
                ('microchip', models.CharField(help_text='15 numbers', max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='the microchip code is 15 numbers long', regex='^\\d{15}$')], verbose_name='Microchip code')),
                ('check_in_date', models.DateField()),
                ('birth_date', models.DateField()),
                ('photo', models.ImageField(blank=True, help_text='Choose the profile picture of the animal', upload_to=animals.models.animal_directory_path)),
                ('box', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='who_lives_here', to='facility.box')),
                ('description', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='animal', to='animals.animaldescription')),
                ('health', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='animal', to='animals.animalhealth')),
                ('management', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='animal', to='animals.animalmanagement')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
