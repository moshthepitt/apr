# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_remove_customer_creator'),
        ('opening_hours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='openinghour',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='customers.Customer', null=True, verbose_name='Customer'),
        ),
    ]
