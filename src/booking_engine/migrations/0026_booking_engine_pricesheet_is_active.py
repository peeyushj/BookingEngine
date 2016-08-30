# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0025_auto_20150511_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
