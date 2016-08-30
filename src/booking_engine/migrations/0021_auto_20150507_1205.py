# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0020_auto_20150507_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
