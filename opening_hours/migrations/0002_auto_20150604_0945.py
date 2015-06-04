# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opening_hours', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together=set([('venue', 'weekday')]),
        ),
        migrations.RemoveField(
            model_name='openinghour',
            name='break_time',
        ),
    ]
