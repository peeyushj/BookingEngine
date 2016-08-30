# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0016_auto_20150507_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='project_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_pricesheet',
            name='as_of_date',
            field=models.DateField(max_length=100),
            preserve_default=True,
        ),
    ]
