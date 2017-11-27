# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0008_auto_20171127_0647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marketgroupmodel',
            old_name='datetime',
            new_name='datetime_created',
        ),
        migrations.AddField(
            model_name='marketgroupmodel',
            name='creation_delay_ms',
            field=models.FloatField(default=0),
        ),
    ]
