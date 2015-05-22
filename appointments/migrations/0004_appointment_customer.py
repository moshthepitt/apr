# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('appointments', '0003_auto_20150423_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name='Customer', to='customers.Customer'),
            preserve_default=False,
        ),
    ]
