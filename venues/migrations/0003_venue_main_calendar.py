# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_auto_20150604_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='main_calendar',
            field=models.BooleanField(default=True, help_text='Should this schedule be displayed in the main Dashboard calendar?', verbose_name='Display in main calendar'),
        ),
    ]
