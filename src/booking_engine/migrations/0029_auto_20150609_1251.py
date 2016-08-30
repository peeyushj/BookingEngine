# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0028_booking_engine_pricesheet_component_is_included_sale_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_booked_payment_plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_plan_id', models.CharField(max_length=50)),
                ('payment_plan_name', models.CharField(max_length=100, null=True)),
                ('payment_plan_description', models.CharField(max_length=100, null=True)),
                ('as_of_date', models.DateField(max_length=100)),
                ('project_id', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'booking_engine_booked_payment_plan',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_booked_payment_plan_milestones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_plan_milestone_id', models.CharField(max_length=50)),
                ('payment_plan_id', models.CharField(max_length=50)),
                ('milestone', models.CharField(max_length=100)),
                ('milestone_free_text', models.CharField(max_length=100)),
                ('milestone_date', models.DateField()),
                ('cost_type', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('formula', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_booked_payment_plan_milestones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_booked_pricesheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pricesheet_id', models.CharField(max_length=50)),
                ('as_of_date', models.DateField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, null=True)),
                ('project_id', models.CharField(max_length=300, null=True)),
            ],
            options={
                'db_table': 'booking_engine_booked_pricesheet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_booked_pricesheet_component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pricesheet_component_id', models.CharField(max_length=50)),
                ('pricesheet_id', models.CharField(max_length=50)),
                ('price_type', models.CharField(max_length=100)),
                ('price_sub_type', models.CharField(max_length=100)),
                ('price_type_free_text', models.CharField(max_length=100)),
                ('price_sub_type_free_text', models.CharField(max_length=100)),
                ('cost_type', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('formula', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_booked_pricesheet_component',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='booking_engine_pricesheet_component',
            name='is_included_sale_value',
        ),
    ]
