# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_subscription_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='can_print',
            field=models.BooleanField(default=False, verbose_name='Can Print'),
        ),
    ]
