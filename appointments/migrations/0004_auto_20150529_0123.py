# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20150528_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='venues.Venue', null=True, verbose_name='Schedule'),
        ),
    ]
