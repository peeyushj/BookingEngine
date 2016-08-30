# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'booking_engine_users',
            },
            bases=(models.Model,),
        ),
    ]
