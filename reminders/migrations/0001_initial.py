# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_appointment_no_reminders'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('client_name', models.CharField(max_length=255, verbose_name='Client Name')),
                ('appointment_time', models.DateTimeField(verbose_name='Appointment Time')),
                ('sent_email', models.BooleanField(default=False, verbose_name='Sent email')),
                ('sent_sms', models.BooleanField(default=False, verbose_name='Sent sms')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Appointment', to='appointments.Appointment', null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
            ],
            options={
                'verbose_name': 'Reminder',
                'verbose_name_plural': 'Reminders',
            },
        ),
    ]
