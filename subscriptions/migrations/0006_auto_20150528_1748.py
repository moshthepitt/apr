# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_subscription_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='customer',
            field=models.OneToOneField(verbose_name='Customer', to='customers.Customer'),
        ),
    ]
