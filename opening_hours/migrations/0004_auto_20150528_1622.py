# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0003_openinghour_break_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='venue',
            field=models.ForeignKey(verbose_name='Venue', to='venues.Venue'),
        ),
    ]
