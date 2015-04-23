# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_venue_creator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['name'], 'verbose_name': 'Clinic', 'verbose_name_plural': 'Clinics'},
        ),
    ]
