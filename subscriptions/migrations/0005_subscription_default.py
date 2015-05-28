# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20150528_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='default',
            field=models.BooleanField(default=False, help_text='The default subscription will be highlighted in price tables.  Ideally only one subscription should be default.', verbose_name='Default'),
        ),
    ]
