# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20150607_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='reminder_sender',
            field=models.EmailField(default=b'no-reply@appointware.com', max_length=254, verbose_name='Reminder from address'),
        ),
    ]
