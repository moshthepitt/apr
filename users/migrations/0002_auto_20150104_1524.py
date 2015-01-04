# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 4, 12, 24, 27, 904279, tzinfo=utc), verbose_name='created on', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 4, 12, 24, 38, 64567, tzinfo=utc), verbose_name='updated on', auto_now=True),
            preserve_default=False,
        ),
    ]
