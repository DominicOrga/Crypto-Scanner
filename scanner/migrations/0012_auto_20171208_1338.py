# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0011_subscriptionmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionmodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
