# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0023_auto_20150507_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='project_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
