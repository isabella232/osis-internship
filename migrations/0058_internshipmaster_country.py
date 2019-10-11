# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-08 14:18
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0016_auto_20170410_1318'),
        ('internship', '0057_auto_20171205_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipmaster',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reference.Country'),
        ),
    ]
