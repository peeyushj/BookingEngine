# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0035_booking_engine_payment_history_mihpayid'),
    ]

    operations = [
        migrations.AddField(
            model_name='booked_payment_plan',
            name='booking_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booked_payment_plan_milestones',
            name='booking_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booked_pricesheet',
            name='booking_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booked_pricesheet_component',
            name='booking_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
