# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-27 08:28
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_auto_20160421_2347'),
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField()),
                ('learning_unit_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitYear')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Organization')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Student')),
            ],
        ),
    ]
