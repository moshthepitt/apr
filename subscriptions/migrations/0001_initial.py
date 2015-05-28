# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_remove_customer_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Subscription Date')),
                ('current_period_start', models.DateTimeField(null=True, verbose_name='Period Start')),
                ('current_period_end', models.DateTimeField(null=True, verbose_name='Period End')),
                ('ended_at', models.DateTimeField(null=True, verbose_name='Ended at', blank=True)),
                ('trial_end', models.DateTimeField(null=True, verbose_name='Trial end', blank=True)),
                ('trial_start', models.DateTimeField(null=True, verbose_name='Trial start', blank=True)),
                ('cancel_at_period_end', models.BooleanField(default=False, verbose_name='Cancel at period end')),
                ('canceled_at', models.DateTimeField(null=True, verbose_name='Canceled at', blank=True)),
                ('cancel_reason', models.TextField(default=None, null=True, verbose_name='Reason for cancelling', blank=True)),
                ('status', models.CharField(default=1, max_length=1, null=True, verbose_name='Status', choices=[(1, 'Trialing'), (2, 'Active'), (3, 'Past Due'), (4, 'Canceled'), (5, 'Unpaid'), (6, 'Ended')])),
                ('customer', models.ForeignKey(verbose_name='Customer', to='customers.Customer')),
            ],
            options={
                'verbose_name': 'Customer Subscription',
                'verbose_name_plural': 'Customer Subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=64, decimal_places=2)),
                ('trial_period', models.PositiveIntegerField(default=15, verbose_name='Trial Period Length', blank=True)),
                ('trial_unit', models.CharField(default=1, max_length=1, verbose_name='Trial Period Units', choices=[(0, 'None'), (1, 'Day'), (2, 'Week'), (3, 'Month'), (4, 'Year')])),
                ('recurring_period', models.PositiveIntegerField(default=1, verbose_name='Recurring Period Length', blank=True)),
                ('recurring_unit', models.CharField(default=3, max_length=1, verbose_name='Recurring Period Units', choices=[(0, 'None'), (1, 'Day'), (2, 'Week'), (3, 'Month'), (4, 'Year')])),
                ('highlighted', models.BooleanField(default=True, help_text='Is this subscription highlighted for prominent display?', verbose_name='Highlighted')),
            ],
            options={
                'ordering': ('price', '-recurring_period'),
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
            },
        ),
        migrations.AddField(
            model_name='customersubscription',
            name='subscription',
            field=models.ForeignKey(verbose_name='Subscription', to='subscriptions.Subscription'),
        ),
        migrations.AlterUniqueTogether(
            name='customersubscription',
            unique_together=set([('customer', 'subscription')]),
        ),
    ]
