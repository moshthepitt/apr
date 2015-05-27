# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150525_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(help_text='Needed to send reminders by email', max_length=254, verbose_name='Email address', blank=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Needed to send reminders by SMS', max_length=255, verbose_name='Phone Number', blank=True),
        ),
    ]
