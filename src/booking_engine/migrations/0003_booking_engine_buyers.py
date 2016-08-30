# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0002_auto_20150429_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_buyers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyer_id', models.CharField(max_length=50)),
                ('buyer_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('pan_card_number', models.CharField(max_length=100)),
                ('buyer_type', models.CharField(max_length=100)),
                ('address_line_1', models.CharField(max_length=300)),
                ('address_line_2', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=300)),
                ('country', models.CharField(max_length=300)),
                ('pincode', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'booking_engine_buyers',
            },
            bases=(models.Model,),
        ),
    ]
