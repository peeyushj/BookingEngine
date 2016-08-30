# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0018_auto_20150507_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_pricesheet',
            name='unit_id',
        ),
    ]
