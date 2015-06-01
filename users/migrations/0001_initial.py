# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('client_id', models.CharField(max_length=255, verbose_name='Client ID', blank=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name', blank=True)),
                ('email', models.EmailField(help_text='Needed to send reminders by email', max_length=254, verbose_name='Email address', blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='Needed to send reminders by SMS', max_length=255, verbose_name='Phone Number', blank=True)),
                ('payment', models.CharField(help_text='How will payment be made?', max_length=1, verbose_name='Payment Method', choices=[(b'1', 'Self'), (b'2', 'Company'), (b'3', 'Insurance')])),
                ('insurance_company', models.CharField(max_length=255, verbose_name='Insurance Company', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this client should be treated as active.', verbose_name='Active')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Customer', to='customers.Customer')),
            ],
            options={
                'ordering': ['client_id'],
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='customers.Customer', null=True, verbose_name='Customer')),
                ('user', models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
