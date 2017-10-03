# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0019_auto_20160928_1621'),
        ('venues', '0011_auto_20150803_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
                ('venues', models.ManyToManyField(to='venues.Venue', verbose_name='Schedules')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'View',
                'verbose_name_plural': 'Views',
            },
        ),
    ]
