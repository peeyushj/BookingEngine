# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0015_auto_20150507_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_history',
            name='is_active',
            field=models.BooleanField(default=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_history',
            name='updated_on',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
