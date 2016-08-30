# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0009_auto_20150506_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_projects',
            name='project_area',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_projects',
            name='project_city',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
