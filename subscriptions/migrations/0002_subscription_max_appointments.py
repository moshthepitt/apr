# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='max_appointments',
            field=models.PositiveIntegerField(default=500, verbose_name='Max Appointments'),
        ),
    ]
