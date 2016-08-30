# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0004_booking_engine_booking_history_booking_engine_bookings_booking_engine_payment_history_booking_engine'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_bookings',
            name='booking_date',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
