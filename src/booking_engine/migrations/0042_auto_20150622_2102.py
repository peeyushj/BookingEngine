# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0041_auto_20150622_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='is_default',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_project_pricesheet',
            name='is_default',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
