# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150410_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['client_id'], 'verbose_name': 'Patient', 'verbose_name_plural': 'Patients'},
        ),
    ]
