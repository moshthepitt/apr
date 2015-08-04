# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0014_auto_20150803_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_active',
            field=models.BooleanField(default=False, help_text='Birthday greetings are sent to clients on their birth days', verbose_name='Activate birthday greetings'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_email',
            field=models.TextField(default='We are thinking of you on this important day and hope that it is filled with happiness. Wishing you many joyous years ahead!', verbose_name='Birthday greeting email message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_send_email',
            field=models.BooleanField(default=True, verbose_name='Birthday greeting send email'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_send_sms',
            field=models.BooleanField(default=True, verbose_name='Birthday greeting send SMS'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_sender',
            field=models.EmailField(default=b'no-reply@appointware.com', max_length=254, verbose_name='Birthday greeting from address'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_sms',
            field=models.CharField(default='Happy Birthday! Wishing you all the best today and always! $OUR_NAME', max_length=255, verbose_name='Birthday greeting SMS message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='birthday_greeting_subject',
            field=models.CharField(default='Happy Birthday, $FIRST_NAME', max_length=100, verbose_name='Birthday greeting subject line'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_active',
            field=models.BooleanField(default=False, help_text='These are booking reminders which are sent to clients a while after their last appointment to encourage them to book a new appointment', verbose_name='Activate Rebooking'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_email',
            field=models.TextField(default='We wanted to remind you that your next appointment is due soon.  Feel free to call us on $OUR_PHONE to book an appointment.', verbose_name='Rebooking email message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_period',
            field=models.PositiveIntegerField(default=6, verbose_name='Rebooking period length', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_period_unit',
            field=models.PositiveIntegerField(default=3, verbose_name='Rebooking period units', choices=[(1, 'Day'), (2, 'Week'), (3, 'Month'), (4, 'Year')]),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_send_email',
            field=models.BooleanField(default=True, verbose_name='Rebooking send email'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_send_sms',
            field=models.BooleanField(default=True, verbose_name='Rebooking send SMS'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_sender',
            field=models.EmailField(default=b'no-reply@appointware.com', max_length=254, verbose_name='Rebooking from address'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_sms',
            field=models.CharField(default='Your next appointment with $OUR_NAME is due soon. Call $OUR_PHONE to book.', max_length=255, verbose_name='Rebooking SMS message'),
        ),
        migrations.AddField(
            model_name='customer',
            name='rebooking_subject',
            field=models.CharField(default='$FIRST_NAME, we miss you', max_length=100, verbose_name='Rebooking subject line'),
        ),
    ]
