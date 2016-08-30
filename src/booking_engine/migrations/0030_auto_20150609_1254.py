# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0029_auto_20150609_1251'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='booking_engine_booked_payment_plan',
            new_name='booked_payment_plan',
        ),
        migrations.RenameModel(
            old_name='booking_engine_booked_payment_plan_milestones',
            new_name='booked_payment_plan_milestones',
        ),
        migrations.RenameModel(
            old_name='booking_engine_booked_pricesheet',
            new_name='booked_pricesheet',
        ),
        migrations.RenameModel(
            old_name='booking_engine_booked_pricesheet_component',
            new_name='booked_pricesheet_component',
        ),
        migrations.AlterModelTable(
            name='booked_payment_plan',
            table='booked_payment_plan',
        ),
        migrations.AlterModelTable(
            name='booked_payment_plan_milestones',
            table='booked_payment_plan_milestones',
        ),
        migrations.AlterModelTable(
            name='booked_pricesheet',
            table='booked_pricesheet',
        ),
        migrations.AlterModelTable(
            name='booked_pricesheet_component',
            table='booked_pricesheet_component',
        ),
    ]
