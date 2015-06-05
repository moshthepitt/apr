# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0003_auto_20150605_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='from_hour',
            field=models.TimeField(null=True, verbose_name='Opening Time', blank=True),
        ),
        migrations.AlterField(
            model_name='openinghour',
            name='to_hour',
            field=models.TimeField(null=True, verbose_name='Closing Time', blank=True),
        ),
    ]
