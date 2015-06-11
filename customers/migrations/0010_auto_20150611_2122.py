# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_auto_20150611_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='send_email',
            field=models.BooleanField(default=True, help_text='Should we send reminders by email?', verbose_name='Email reminder'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='send_sms',
            field=models.BooleanField(default=True, help_text='Should we send reminders by text message (SMS)?', verbose_name='SMS reminder'),
        ),
    ]
