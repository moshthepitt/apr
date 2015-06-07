# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='custom_reminder',
            field=models.BooleanField(default=False, verbose_name='Use custom reminder'),
        ),
        migrations.AddField(
            model_name='customer',
            name='reminder_email',
            field=models.TextField(default='We wanted to remind you that you have an appointment at $OUR_NAME on $APPOINTMENT_DATE from $APPOINTMENT_START_TIME. Please be on time.', verbose_name='Reminder email message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='reminder_sender',
            field=models.EmailField(default=b'no-reply <no-reply@appointware.com>', max_length=254, verbose_name='Reminder from address'),
        ),
        migrations.AddField(
            model_name='customer',
            name='reminder_sms',
            field=models.CharField(default='Reminder! Appointment with $OUR_NAME on $APPOINTMENT_DATE from $APPOINTMENT_START_TIME', max_length=255, verbose_name='Reminder SMS message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='reminder_subject',
            field=models.CharField(default='Reminder Appointment with $OUR_NAME at $APPOINTMENT_DATE from $APPOINTMENT_START_TIME', max_length=100, verbose_name='Reminder subject line'),
        ),
        migrations.AddField(
            model_name='customer',
            name='show_cancel_link',
            field=models.BooleanField(default=True, verbose_name='Show a link to cancel appointment'),
        ),
        migrations.AddField(
            model_name='customer',
            name='show_confirm_link',
            field=models.BooleanField(default=True, verbose_name='Show a link to confirm appointment'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created on'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated on'),
        ),
    ]
