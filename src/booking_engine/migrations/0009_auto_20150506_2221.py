# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0008_booking_engine_projects_project_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_engine_project_contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_id', models.CharField(max_length=50)),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=100)),
                ('contact_email', models.CharField(max_length=100)),
                ('contact_type', models.CharField(max_length=100)),
                ('project_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'booking_engine_project_contacts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking_engine_projects',
            name='builder_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
