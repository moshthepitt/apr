# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_doctor_creator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['first_name'], 'verbose_name': 'Doctor', 'verbose_name_plural': 'Doctor'},
        ),
    ]
