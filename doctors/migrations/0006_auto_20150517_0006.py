# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_auto_20150503_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['first_name'], 'verbose_name': 'Doctor', 'verbose_name_plural': 'Doctors'},
        ),
        migrations.AlterField(
            model_name='doctor',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email address', blank=True),
        ),
    ]
