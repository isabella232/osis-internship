# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 09:23
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


def linkToDefaultCohort(apps, schema_editor):
    Cohort = apps.get_model("internship", "Cohort")
    InternshipOffer = apps.get_model("internship", "InternshipOffer")
    db_alias = schema_editor.connection.alias
    default_cohort = Cohort.objects.first()
    InternshipOffer.objects.all().update(cohort=default_cohort)

class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0012_cohort'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipoffer',
            name='cohort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='internship.Cohort'),
            preserve_default=False
        ),
        migrations.RunPython(linkToDefaultCohort),
        migrations.AlterField(
            model_name='internshipoffer',
            name='cohort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.Cohort'),
            preserve_default=False
        )
    ]
