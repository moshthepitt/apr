# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('users', '0001_initial'),
        ('venues', '0001_initial'),
        ('doctors', '0001_initial'),
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('status', models.CharField(default=b'scheduled', max_length=15, verbose_name='Status', choices=[(b'scheduled', 'Scheduled'), (b'confirmed', 'Confirmed'), (b'canceled', 'Canceled'), (b'notified', 'Notified'), (b'noshow', 'No Show'), (b'showed', 'Showed Up')])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Client', to='users.Client')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='doctors.Doctor', null=True, verbose_name='Doctor')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Event', to='schedule.Event')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='venues.Venue', null=True, verbose_name='Schedule')),
            ],
            options={
                'ordering': ['-event__start'],
            },
        ),
    ]
