# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0048_auto_20150729_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_project_types',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_type_id', models.CharField(max_length=50)),
                ('project_type_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_project_types',
            },
            bases=(models.Model,),
        ),
    ]
