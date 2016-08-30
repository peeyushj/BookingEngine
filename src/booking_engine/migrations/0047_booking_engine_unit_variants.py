# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0046_auto_20150715_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_unit_variants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_variant_id', models.CharField(max_length=50)),
                ('project_id', models.CharField(max_length=50)),
                ('unit_variant_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_unit_variants',
            },
            bases=(models.Model,),
        ),
    ]
