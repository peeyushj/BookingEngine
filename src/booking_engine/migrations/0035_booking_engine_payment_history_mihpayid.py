# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0034_auto_20150609_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_payment_history',
            name='mihpayid',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
