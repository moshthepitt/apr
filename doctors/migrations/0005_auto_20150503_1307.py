# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctors', '0004_auto_20150423_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to=settings.AUTH_USER_MODEL, blank=True, help_text='This user will be able to log in as this doctor', null=True, verbose_name='User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='doctor',
            name='creator',
            field=models.ForeignKey(related_name='doctor_creator', on_delete=django.db.models.deletion.PROTECT, verbose_name='Creator', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
