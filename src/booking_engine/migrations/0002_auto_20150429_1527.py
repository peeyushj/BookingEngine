# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_users',
            name='is_active',
        ),
        migrations.AddField(
            model_name='booking_engine_users',
            name='create_date',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_users',
            name='password',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
