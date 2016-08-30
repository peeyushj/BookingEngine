# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0021_auto_20150507_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='payment_plan_description',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='payment_plan_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
