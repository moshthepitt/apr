# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_client_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.CharField(help_text='Optional unique client ID', unique=True, max_length=255, verbose_name='Client ID', blank=True),
        ),
    ]
