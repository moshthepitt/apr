# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150527_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['client_id'], 'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.CharField(max_length=255, verbose_name='Client ID', blank=True),
        ),
    ]
