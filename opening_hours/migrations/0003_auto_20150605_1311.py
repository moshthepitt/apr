# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0002_auto_20150604_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='from_hour',
            field=models.TimeField(null=True, verbose_name='From Hour', blank=True),
        ),
        migrations.AlterField(
            model_name='openinghour',
            name='to_hour',
            field=models.TimeField(null=True, verbose_name='To Hour', blank=True),
        ),
    ]
