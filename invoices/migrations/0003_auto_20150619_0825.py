# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_auto_20150619_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='upgrade_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to='subscriptions.Subscription', blank=True, help_text='Use this field in case the payment was for a subscription upgrade/downgrade', null=True, verbose_name='Upgrade to Subscription'),
        ),
    ]
