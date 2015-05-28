# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscription_max_appointments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='status',
            field=models.PositiveIntegerField(default=1, max_length=1, null=True, verbose_name='Status', choices=[(1, 'Trialing'), (2, 'Active'), (3, 'Past Due'), (4, 'Canceled'), (5, 'Unpaid'), (6, 'Ended')]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='recurring_unit',
            field=models.PositiveIntegerField(default=3, max_length=1, verbose_name='Recurring Period Units', choices=[(0, 'None'), (1, 'Day'), (2, 'Week'), (3, 'Month'), (4, 'Year')]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='trial_unit',
            field=models.PositiveIntegerField(default=1, max_length=1, verbose_name='Trial Period Units', choices=[(0, 'None'), (1, 'Day'), (2, 'Week'), (3, 'Month'), (4, 'Year')]),
        ),
    ]
