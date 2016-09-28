# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0018_auto_20150907_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='time_slot_height',
            field=models.IntegerField(default=25, help_text='The height of each timeslot in pixels. Calendar event text is scaled relative to the timeslot height.', verbose_name='Time Slot Height'),
        ),
        migrations.AddField(
            model_name='customer',
            name='time_slots_per_hour',
            field=models.IntegerField(default=4, help_text='The number of timeslots that will be available within an hour.', verbose_name='Time Slots Per Hour'),
        ),
    ]
