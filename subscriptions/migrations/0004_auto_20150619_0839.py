# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20150619_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='current_period_end',
            field=models.DateTimeField(default=None, null=True, verbose_name='Period End', blank=True),
        ),
        migrations.AlterField(
            model_name='customersubscription',
            name='current_period_start',
            field=models.DateTimeField(default=None, null=True, verbose_name='Period Start', blank=True),
        ),
    ]
