##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.db import models
from osis_common.models.serializable_model import SerializableModelAdmin, SerializableModel

from internship.admin_actions.actions import export_as_csv_action

class InternshipChoiceAdmin(SerializableModelAdmin):
    list_display = ('id', 'student', 'organization', 'speciality', 'choice', 'internship', 'priority', 'uuid')
    fieldsets = ((None, {'fields': ('id', 'student', 'organization', 'speciality', 'choice', 'internship',
                                    'priority')}),)
    raw_id_fields = ('student', 'organization', 'speciality')
    search_fields = ['id', 'uuid', 'student__person__first_name', 'student__person__last_name']

    actions = [export_as_csv_action("Export to CSV",
        fields = [
            'student',
            'organization',
            'speciality',
            'internship',
            'choice',
            'priority',
            'uuid'
        ]
    )]


class InternshipChoice(SerializableModel):
    student = models.ForeignKey('base.Student')
    organization = models.ForeignKey('internship.Organization')
    speciality = models.ForeignKey('internship.InternshipSpeciality', null=True)
    choice = models.IntegerField()
    internship = models.ForeignKey('internship.Internship')
    priority = models.BooleanField()

    def __str__(self):
        return u"%s - %s : %s" % (self.organization.acronym, self.speciality.acronym, self.choice)

    class Meta:
        unique_together = (("student", "internship", "choice"),)


def search(student=None, speciality=None, specialities=None, internship=None):
    has_criteria = False
    queryset = InternshipChoice.objects

    if student:
        queryset = queryset.filter(student=student)
        has_criteria = True

    if speciality:
        queryset = queryset.filter(speciality=speciality)
        has_criteria = True

    if internship:
        queryset = queryset.filter(internship=internship)
        has_criteria = True

    if specialities:
        queryset = queryset.filter(speciality_id__in=specialities)
        has_criteria = True

    if has_criteria:
        return queryset
    else:
        return None


def get_number_first_choice_by_organization(speciality):
    return InternshipChoice.objects.filter(choice=1, speciality=speciality).values("organization")\
        .annotate(models.Count("organization"))
