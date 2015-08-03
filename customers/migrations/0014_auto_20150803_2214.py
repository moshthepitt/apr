# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_auto_20150708_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='client_display',
            field=models.CharField(default=b'1', help_text='How should the client be represented in the calendar?', max_length=1, verbose_name='Client Display', choices=[(b'1', 'Client Name'), (b'2', 'Client Phone'), (b'3', 'Client Email'), (b'4', 'Client ID'), (b'5', 'Client Name & Client ID'), (b'6', 'Client Name, Client Phone & Client ID'), (b'7', 'Appointment Title')]),
        ),
    ]
