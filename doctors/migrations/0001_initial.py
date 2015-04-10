# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
                ('email', models.EmailField(max_length=75, verbose_name='Email address', blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name='Phone Number', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this doctor should be treated as active.', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctor',
            },
            bases=(models.Model,),
        ),
    ]
