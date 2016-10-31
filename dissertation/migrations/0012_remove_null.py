# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-11 11:22
from __future__ import unicode_literals
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0011_populate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propositionoffer',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
