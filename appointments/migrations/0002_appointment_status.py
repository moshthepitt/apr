# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(default=b'scheduled', max_length=15, verbose_name='Status', choices=[(b'scheduled', 'Scheduled'), (b'confirmed', 'Confirmed'), (b'canceled', 'Canceled'), (b'notified', 'Notified'), (b'noshow', 'No Show')]),
        ),
    ]
