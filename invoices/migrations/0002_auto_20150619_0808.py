# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscription_max_schedules'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='upgrade_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, to='subscriptions.Subscription', blank=True, help_text='Use this field in case the payment was for a subscription upgrade/downgrade', null=True, verbose_name='Subscription'),
        ),
        migrations.AlterField(
            model_name='mpesareceipt',
            name='receipt',
            field=models.CharField(unique=True, max_length=50, verbose_name='MPESA Confirmation Code'),
        ),
    ]
