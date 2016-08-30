# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0007_booking_engine_units_price_per_sqft'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_projects',
            name='project_type',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
