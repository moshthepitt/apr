# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150410_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_id',
            field=models.CharField(max_length=255, verbose_name='File Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='insurance_company',
            field=models.CharField(max_length=255, verbose_name='Insurance Company', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='payment',
            field=models.CharField(default=1, help_text='How will payment be made?', max_length=1, verbose_name='Payment Method', choices=[(b'1', 'Self'), (b'2', 'Company'), (b'3', 'Insurance')]),
            preserve_default=False,
        ),
    ]
