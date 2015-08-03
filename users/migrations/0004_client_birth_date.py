# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150730_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='birth_date',
            field=models.DateField(default=None, help_text='Needed to send birthday greetings', null=True, verbose_name='Date of Birth', blank=True),
        ),
    ]
