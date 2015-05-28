# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20150528_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='status',
            field=models.PositiveIntegerField(default=1, verbose_name='Status', choices=[(1, 'Trialing'), (2, 'Active'), (3, 'Past Due'), (4, 'Canceled'), (5, 'Unpaid'), (6, 'Ended')]),
        ),
    ]
