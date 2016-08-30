# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0010_auto_20150506_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking_engine_project_contacts',
            old_name='contact_type',
            new_name='contact_designation',
        ),
        migrations.AddField(
            model_name='booking_engine_project_contacts',
            name='is_primary',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
