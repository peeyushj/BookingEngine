# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0017_auto_20150507_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking_engine_pricesheet',
            old_name='project_id',
            new_name='unit_id',
        ),
    ]
