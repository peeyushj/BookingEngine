# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0042_auto_20150622_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_project_pricesheet',
            name='is_default',
        ),
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='is_default',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
