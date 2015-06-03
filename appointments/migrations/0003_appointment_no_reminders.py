# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_appointment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='no_reminders',
            field=models.BooleanField(default=False, help_text='Do not send reminders for this appointment', verbose_name='No Reminders'),
        ),
    ]
