# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-25 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0030_auto_20180125_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internshipstudentinformation',
            name='contest',
            field=models.CharField(choices=[('SPECIALIST', 'specialist'), ('GENERALIST', 'generalist')], max_length=124, null=True),
        ),
    ]
