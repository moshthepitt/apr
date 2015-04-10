# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
        ('doctors', '0001_initial'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='doctors.Doctor', null=True, verbose_name='Doctor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='venues.Venue', null=True, verbose_name='Clinic'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Patient', to='users.Client'),
            preserve_default=True,
        ),
    ]
