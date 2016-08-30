# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0032_auto_20150609_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='booked_payment_plan_milestones',
            name='entered_value',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booked_pricesheet_component',
            name='entered_value',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
