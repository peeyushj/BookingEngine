# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0012_auto_20150507_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_booking_history',
            name='updated_on',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
