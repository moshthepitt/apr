# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Client', to='users.Client'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(default=b'scheduled', max_length=15, verbose_name='Status', choices=[(b'scheduled', 'Scheduled'), (b'confirmed', 'Confirmed'), (b'canceled', 'Canceled'), (b'notified', 'Notified'), (b'noshow', 'No Show'), (b'showed', 'Showed Up')]),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='venues.Venue', null=True, verbose_name='Venue'),
        ),
    ]
