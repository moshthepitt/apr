# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0016_customer_use_tags'),
        ('appointments', '0005_auto_20150816_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer', null=True),
        ),
    ]
