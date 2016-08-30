# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0011_auto_20150507_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_project_contacts',
            name='is_primary',
            field=models.BooleanField(default=True, max_length=100),
            preserve_default=True,
        ),
    ]
