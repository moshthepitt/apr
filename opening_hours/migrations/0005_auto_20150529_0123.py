# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0004_auto_20150528_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='venue',
            field=models.ForeignKey(verbose_name='Schedule', to='venues.Venue'),
        ),
    ]
