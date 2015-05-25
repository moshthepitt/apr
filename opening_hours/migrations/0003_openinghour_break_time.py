# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0002_openinghour_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='openinghour',
            name='break_time',
            field=models.BooleanField(default=False, help_text='Does this time represent a break e.g. lunch break', verbose_name='Break'),
        ),
    ]
