# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 15:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rsi',
            new_name='RsiModel',
        ),
    ]