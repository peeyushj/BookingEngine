# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0003_booking_engine_buyers'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_booking_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('booking_history_id', models.CharField(max_length=50)),
                ('booking_id', models.CharField(max_length=50)),
                ('old_status', models.CharField(max_length=100)),
                ('new_status', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=50)),
                ('updated_on', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_booking_history',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_bookings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('booking_id', models.CharField(max_length=50)),
                ('buyer_id', models.CharField(max_length=50)),
                ('unit_id', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_bookings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_payment_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_history_id', models.CharField(max_length=50)),
                ('booking_id', models.CharField(max_length=50)),
                ('payment_status', models.CharField(max_length=100)),
                ('is_active', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_payment_history',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_payment_plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_plan_id', models.CharField(max_length=50)),
                ('price_sheet_id', models.CharField(max_length=100)),
                ('broker_id', models.CharField(max_length=100)),
                ('as_of_date', models.CharField(max_length=100)),
                ('is_active', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_payment_plan',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_payment_plan_milestones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_plan_milestone_id', models.CharField(max_length=50)),
                ('payment_plan_id', models.CharField(max_length=50)),
                ('milestone', models.CharField(max_length=100)),
                ('milestone_free_text', models.CharField(max_length=100)),
                ('milestone_date', models.CharField(max_length=100)),
                ('cost_type', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('formula', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_payment_plan_milestones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_pricesheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pricesheet_id', models.CharField(max_length=50)),
                ('as_of_date', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_pricesheet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_pricesheet_component',
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
                'db_table': 'booking_engine_pricesheet_component',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_project_payment_plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_payment_plan_id', models.CharField(max_length=50)),
                ('payment_plan_id', models.CharField(max_length=50)),
                ('project_id', models.CharField(max_length=100)),
                ('broker_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_project_payment_plan',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_project_pricesheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_pricesheet_id', models.CharField(max_length=50)),
                ('project_id', models.CharField(max_length=50)),
                ('pricesheet_id', models.CharField(max_length=50)),
                ('broker_id', models.CharField(max_length=100)),
                ('is_active', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_project_pricesheet',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.CharField(max_length=50)),
                ('project_name', models.CharField(max_length=100)),
                ('payment_plan_id', models.CharField(max_length=100)),
                ('price_sheet_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_towers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tower_id', models.CharField(max_length=50)),
                ('project_id', models.CharField(max_length=50)),
                ('tower_name', models.CharField(max_length=100)),
                ('no_of_floors', models.CharField(max_length=100)),
                ('total_units', models.CharField(max_length=100)),
                ('total_units_in_floor', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_towers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='booking_engine_units',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_id', models.CharField(max_length=50)),
                ('project_id', models.CharField(max_length=50)),
                ('tower_id', models.CharField(max_length=50)),
                ('floor_number', models.CharField(max_length=100)),
                ('door_number', models.CharField(max_length=100)),
                ('Availability', models.CharField(max_length=100)),
                ('booking_amount', models.CharField(max_length=100)),
                ('payment_plan_id', models.CharField(max_length=100)),
                ('price_sheet_id', models.CharField(max_length=100)),
                ('super_builtup_area', models.CharField(max_length=100)),
                ('builtup_area', models.CharField(max_length=100)),
                ('carpet_area', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_units',
            },
            bases=(models.Model,),
        ),
    ]
