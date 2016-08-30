# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0047_booking_engine_unit_variants'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_brokers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('broker_id', models.CharField(max_length=50)),
                ('broker_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_brokers',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='broker_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='project_type_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='tower_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='unit_variant_id',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
