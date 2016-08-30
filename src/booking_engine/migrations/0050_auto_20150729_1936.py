# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0049_booking_engine_project_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='broker_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='project_type_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='tower_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='unit_variant_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
