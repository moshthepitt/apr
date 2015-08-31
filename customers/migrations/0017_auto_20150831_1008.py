# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0016_customer_use_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='use_four_day',
            field=models.BooleanField(default=False, verbose_name='Activate Four-day View'),
        ),
        migrations.AddField(
            model_name='customer',
            name='use_no_background_print',
            field=models.BooleanField(default=False, verbose_name='No background color on print'),
        ),
    ]
