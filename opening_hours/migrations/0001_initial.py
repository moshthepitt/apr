# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.IntegerField(verbose_name='Weekday', choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('from_hour', models.TimeField(verbose_name='From Hour')),
                ('to_hour', models.TimeField(verbose_name='To Hour')),
                ('break_time', models.BooleanField(default=False, help_text='Does this time represent a break e.g. lunch break', verbose_name='Break')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='customers.Customer', null=True, verbose_name='Customer')),
                ('venue', models.ForeignKey(verbose_name='Schedule', to='venues.Venue')),
            ],
            options={
                'ordering': ['venue__name', 'weekday', 'from_hour'],
                'verbose_name': 'Opening Hour',
                'verbose_name_plural': 'Opening Hours',
            },
        ),
    ]
