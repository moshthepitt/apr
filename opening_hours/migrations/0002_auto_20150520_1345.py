# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0003_auto_20150423_1814'),
        ('opening_hours', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.IntegerField(verbose_name='Weekday', choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('from_hour', models.TimeField(verbose_name='From Hour')),
                ('to_hour', models.TimeField(verbose_name='To Hour')),
                ('venue', models.ForeignKey(verbose_name='Clinic', to='venues.Venue')),
            ],
            options={
                'ordering': ['weekday'],
                'verbose_name': 'Opening Hour',
                'verbose_name_plural': 'Opening Hours',
            },
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='venue',
        ),
        migrations.DeleteModel(
            name='OpeningHours',
        ),
    ]
