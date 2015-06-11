# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_auto_20150607_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='allow_overlap',
            field=models.BooleanField(default=False, help_text='Should we allow two or more appointments at the same time?', verbose_name='Allow appointment overlap'),
        ),
        migrations.AddField(
            model_name='customer',
            name='send_email',
            field=models.BooleanField(default=True, verbose_name='Send email reminder'),
        ),
        migrations.AddField(
            model_name='customer',
            name='send_sms',
            field=models.BooleanField(default=True, verbose_name='Send text message reminder'),
        ),
    ]
