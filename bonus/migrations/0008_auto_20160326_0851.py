# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 08:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bonus', '0007_auto_20160326_0839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='recvNum',
            new_name='recvBonusSum',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='sendNum',
            new_name='sendBonusSum',
        ),
    ]