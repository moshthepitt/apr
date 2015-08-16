# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_appointment_no_reminders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('color', models.CharField(max_length=50, verbose_name='Color')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='tag',
            field=models.ForeignKey(default=None, blank=True, to='appointments.Tag', null=True, verbose_name='Tag'),
        ),
    ]
