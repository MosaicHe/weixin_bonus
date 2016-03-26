# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bonus', '0004_auto_20160323_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus_content',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bonus.Good'),
        ),
        migrations.AlterField(
            model_name='bonus_content',
            name='quantity',
            field=models.IntegerField(default=5),
        ),
    ]