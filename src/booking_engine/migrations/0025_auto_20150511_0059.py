# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0024_booking_engine_payment_plan_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='description',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='project_id',
            field=models.CharField(max_length=6, null=True),
            preserve_default=True,
        ),
    ]
