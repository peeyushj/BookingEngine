# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0027_auto_20150511_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_pricesheet_component',
            name='is_included_sale_value',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
