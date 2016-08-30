# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0043_auto_20150622_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_units',
            name='payment_plan_id',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_units',
            name='price_sheet_id',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
