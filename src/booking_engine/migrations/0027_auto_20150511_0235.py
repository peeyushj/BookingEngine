# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0026_booking_engine_pricesheet_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_users',
            name='email',
        ),
        migrations.RemoveField(
            model_name='booking_engine_users',
            name='name',
        ),
        migrations.RemoveField(
            model_name='booking_engine_users',
            name='password',
        ),
        migrations.AddField(
            model_name='booking_engine_users',
            name='user_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
