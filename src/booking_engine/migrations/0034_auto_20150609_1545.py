# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0033_auto_20150609_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_payment_plan',
            name='broker_id',
        ),
        migrations.RemoveField(
            model_name='booking_engine_payment_plan',
            name='price_sheet_id',
        ),
    ]
