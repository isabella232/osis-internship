# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 07:28
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0037_add_cohort_to_student_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationaddress',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', related_query_name='address', to='internship.Organization'),
        ),
    ]
