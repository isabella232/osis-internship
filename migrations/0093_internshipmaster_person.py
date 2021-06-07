# Generated by Django 3.1.1 on 2020-11-30 16:17
import django.db.models.deletion
import uuid
from django.db import migrations, models
from django.db.migrations import RunPython

from base.models.enums import person_source_type


def create_persons(apps, schema_editor):
    InternshipMaster = apps.get_model('internship', 'InternshipMaster')
    Person = apps.get_model('base', 'Person')

    master_fields = {field.name for field in InternshipMaster._meta.fields}
    person_fields = {field.name for field in Person._meta.fields}
    common_fields = master_fields.intersection(person_fields).difference({'uuid', 'id', 'email'})

    for master in InternshipMaster.objects.all():
        # check master has already a person in db that should be linked to
        master_email = master.email or master.email_private
        if master_email and Person.objects.filter(email=master_email).exists():
            existing_person = Person.objects.filter(email=master_email).first()
            for field, value in {field: getattr(master, field) for field in common_fields}.items():
                if not getattr(existing_person, field):
                    setattr(existing_person, field, value)
            existing_person.save()
            master.person_id = existing_person.id
            master.save()
        # create person when none exist
        elif not master.person_id and master_email:
            person_instance = Person.objects.create(
                uuid=uuid.uuid4(),
                email=master_email,
                **{field: getattr(master, field) for field in common_fields},
                source=person_source_type.INTERNSHIP
            )
            master.person = person_instance
            master.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0543_auto_20201120_1040'),
        ('internship', '0092_clean_master_duplicates'),
    ]

    operations = [
        # link to person fk
        migrations.AddField(
            model_name='internshipmaster',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='base.person'),
        ),
        # create persons based on data
        migrations.RunPython(create_persons, RunPython.noop, elidable=True),
        # remove fields that are available in Person table
        migrations.RemoveField(
            model_name='internshipmaster',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='email',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='internshipmaster',
            name='phone_mobile',
        ),
    ]
