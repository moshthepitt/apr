# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import randomslugfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='slug',
            field=randomslugfield.fields.RandomSlugField(editable=False, length=9, max_length=9, blank=True, unique=True),
        ),
    ]
