# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20150619_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-date'], 'verbose_name': 'Invoice', 'verbose_name_plural': 'Invoices'},
        ),
    ]
