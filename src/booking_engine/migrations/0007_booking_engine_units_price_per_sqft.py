# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0006_booking_engine_payment_history_updated_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_units',
            name='price_per_sqft',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
