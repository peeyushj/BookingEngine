# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0037_auto_20150619_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_projects',
            name='default_payment_plan_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_projects',
            name='default_price_sheet_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
