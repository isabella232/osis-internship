# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 21:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from internship.models.cohort import Cohort
from internship.models.affectation_generation_time import AffectationGenerationTime

def assign_first_cohort_to_periods(apps, schema_editor):
    cohort = Cohort.objects.first()

    AffectationGenerationTime.objects.all().update(cohort=cohort)

class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0047_auto_20170410_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='affectationgenerationtime',
            name='cohort',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='internship.Cohort'),
        ),
        migrations.RunPython(assign_first_cohort_to_periods),
        migrations.AlterField(
            model_name='affectationgenerationtime',
            name='cohort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.Cohort'),
        )
    ]
