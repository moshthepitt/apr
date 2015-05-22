# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('users', '0007_auto_20150517_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name='Customer', to='customers.Customer'),
            preserve_default=False,
        ),
    ]
