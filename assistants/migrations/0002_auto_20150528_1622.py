# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistants', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assistant',
            options={'ordering': ['first_name'], 'verbose_name': 'Assistant', 'verbose_name_plural': 'Assistants'},
        ),
    ]
