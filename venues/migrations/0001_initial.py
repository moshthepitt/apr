# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('name', models.CharField(max_length=255, verbose_name='Venue name', blank=True)),
            ],
            options={
                'verbose_name': 'Clinic',
                'verbose_name_plural': 'Clinics',
            },
            bases=(models.Model,),
        ),
    ]
