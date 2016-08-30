# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0039_auto_20150622_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_units',
            name='unit_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
