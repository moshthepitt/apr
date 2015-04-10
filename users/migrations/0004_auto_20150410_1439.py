# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150410_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(unique=True, max_length=255, verbose_name='Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together=set([]),
        ),
    ]
