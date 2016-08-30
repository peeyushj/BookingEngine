# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0013_auto_20150507_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_booking_history',
            name='updated_on',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
