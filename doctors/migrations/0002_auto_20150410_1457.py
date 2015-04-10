# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=255, verbose_name='Phone Number', blank=True),
            preserve_default=True,
        ),
    ]
