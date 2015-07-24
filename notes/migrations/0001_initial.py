# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0010_auto_20150708_1457'),
        ('customers', '0013_auto_20150708_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('date', models.DateField(verbose_name='Date')),
                ('note', models.TextField(verbose_name='Note')),
                ('note_type', models.CharField(default=b'2', max_length=1, verbose_name='Type', choices=[(b'1', 'Top'), (b'2', 'Bottom')])),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='venues.Venue', null=True, verbose_name='Schedule')),
            ],
            options={
                'ordering': ['-date', 'id'],
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
    ]
