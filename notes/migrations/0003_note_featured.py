# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20150907_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
    ]
