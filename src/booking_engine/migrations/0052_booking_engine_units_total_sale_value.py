# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0051_auto_20150730_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_units',
            name='total_sale_value',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
