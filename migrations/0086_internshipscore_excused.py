# Generated by Django 2.2.5 on 2020-03-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0085_auto_20191118_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipscore',
            name='excused',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
