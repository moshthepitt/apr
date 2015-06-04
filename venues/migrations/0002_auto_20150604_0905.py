# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this schedule should be treated as active.', verbose_name='Active'),
        ),
    ]
