# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email address', blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=255, verbose_name='Phone Number', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this doctor should be treated as active.', verbose_name='Active')),
                ('creator', models.ForeignKey(related_name='doctor_creator', on_delete=django.db.models.deletion.PROTECT, verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to=settings.AUTH_USER_MODEL, blank=True, help_text='This user will be able to log in as this doctor', null=True, verbose_name='User')),
            ],
            options={
                'ordering': ['first_name'],
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
    ]
