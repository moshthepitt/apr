# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0002_auto_20150520_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ['venue__name', 'weekday', 'from_hour'], 'verbose_name': 'Opening Hour', 'verbose_name_plural': 'Opening Hours'},
        ),
    ]
