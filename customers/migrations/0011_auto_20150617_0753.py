# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0010_auto_20150611_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this customer should be treated as active.', verbose_name='Active'),
        ),
    ]
