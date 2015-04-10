# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Patient', 'verbose_name_plural': 'Patients'},
        ),
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Phone Number', blank=True),
            preserve_default=True,
        ),
    ]
