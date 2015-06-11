# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0006_venue_shown_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='allow_overlap',
            field=models.BooleanField(default=False, help_text='Should we allow two or more appointments at the same time?', verbose_name='Allow appointment overlap'),
        ),
        migrations.AddField(
            model_name='venue',
            name='send_email',
            field=models.BooleanField(default=True, verbose_name='Send email reminder'),
        ),
        migrations.AddField(
            model_name='venue',
            name='send_sms',
            field=models.BooleanField(default=True, verbose_name='Send text message reminder'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Schedule', blank=True),
        ),
    ]
