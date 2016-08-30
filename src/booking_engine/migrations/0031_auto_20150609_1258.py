# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0030_auto_20150609_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booked_payment_plan_milestones',
            old_name='amount',
            new_name='total_amount',
        ),
        migrations.RenameField(
            model_name='booked_pricesheet_component',
            old_name='amount',
            new_name='total_amount',
        ),
    ]
