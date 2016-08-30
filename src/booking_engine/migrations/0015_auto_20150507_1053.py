# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0014_auto_20150507_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking_engine_payment_history',
            old_name='payment_history_id',
            new_name='payment_id',
        ),
    ]
