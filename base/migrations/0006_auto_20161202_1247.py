# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-02 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20161202_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningunitcomponent',
            name='type',
            field=models.CharField(blank=True, choices=[('LECTURING', 'LECTURING'), ('PRACTICAL_EXERCISES', 'PRACTICAL_EXERCISES')], max_length=25, null=True),
        ),
    ]
