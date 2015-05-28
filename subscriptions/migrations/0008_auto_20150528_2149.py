# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_auto_20150528_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersubscription',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 18, 49, 28, 303897, tzinfo=utc), verbose_name='created on', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customersubscription',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 18, 49, 36, 662801, tzinfo=utc), verbose_name='updated on', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 18, 49, 42, 221906, tzinfo=utc), verbose_name='created on', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 18, 49, 49, 186239, tzinfo=utc), verbose_name='updated on', auto_now=True),
            preserve_default=False,
        ),
    ]
