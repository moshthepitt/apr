# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0017_auto_20150831_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='use_four_day',
            field=models.BooleanField(default=False, verbose_name='Activate Three-day View'),
        ),
    ]
