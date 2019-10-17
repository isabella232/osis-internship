# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-19 15:51
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0025_affectationgenerationtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipSpecialityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipSpecialityGroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.InternshipSpecialityGroup')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.InternshipSpeciality')),
            ],
        ),
    ]
