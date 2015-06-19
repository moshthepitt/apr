# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_auto_20150617_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('date', models.DateField(verbose_name='Date')),
                ('name', models.CharField(max_length=255, verbose_name='Name of payee', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=64, decimal_places=2)),
                ('currency', models.CharField(default='KES', max_length=3, verbose_name='Currency')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=None, max_digits=64, blank=True, null=True, verbose_name='Paid amount')),
                ('paid_currency', models.CharField(default=None, max_length=3, null=True, verbose_name='Paid currency', blank=True)),
                ('processing_fee', models.DecimalField(decimal_places=2, default=None, max_digits=64, blank=True, null=True, verbose_name='Processing fee')),
                ('status', models.CharField(default=b'3', max_length=1, verbose_name='Status', choices=[('1', 'Paid'), ('2', 'Canceled'), ('3', 'Pending'), ('4', 'Failed'), ('5', 'Partly Paid')])),
                ('method', models.CharField(max_length=1, verbose_name='Method', choices=[('1', 'Cash'), ('2', 'Cheque'), ('3', 'Lipa na MPESA')])),
                ('subscription_period_start', models.DateTimeField(default=None, null=True, verbose_name='Subscription Period Start', blank=True)),
                ('subscription_period_end', models.DateTimeField(default=None, null=True, verbose_name='Subscription Period End', blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='MPESAReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('receipt', models.CharField(max_length=50, verbose_name='MPESA Confirmation Code')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Invoice', to='invoices.Invoice')),
            ],
            options={
                'verbose_name': 'MPESA Receipt',
                'verbose_name_plural': 'MPESA Receipts',
            },
        ),
    ]
