# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150705_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default=b'1', max_length=1, verbose_name='Role', choices=[(b'1', 'Admin'), (b'2', 'Editor'), (b'3', 'User')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='staff',
            field=models.BooleanField(default=False, verbose_name='Staff Member'),
        ),
    ]
