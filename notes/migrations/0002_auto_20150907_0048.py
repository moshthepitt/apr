# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_type',
            field=models.CharField(default=b'1', max_length=1, verbose_name='Type', choices=[(b'1', 'Top'), (b'2', 'Bottom')]),
        ),
    ]
