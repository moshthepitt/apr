# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0015_auto_20150804_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='use_tags',
            field=models.BooleanField(default=False, help_text='Tags are used to classify appointments', verbose_name='Use Tags'),
        ),
    ]
