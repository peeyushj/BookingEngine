# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0022_auto_20150507_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_plan_milestones',
            name='milestone_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
