# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0003_auto_20150528_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['name'], 'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
    ]
