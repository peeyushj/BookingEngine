# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0036_auto_20150613_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_projects',
            name='payment_plan_id',
        ),
        migrations.RemoveField(
            model_name='booking_engine_projects',
            name='price_sheet_id',
        ),
    ]
