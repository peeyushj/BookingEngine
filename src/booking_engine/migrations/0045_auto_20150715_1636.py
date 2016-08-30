# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0044_auto_20150622_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked_payment_plan_milestones',
            name='milestone_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_plan_milestones',
            name='milestone_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
