# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaulttags import register as reg

register = template.Library()


@register.assignment_tag
def choice_for_offer(internship_choices, offer, internship):
    try:
        choice = internship_choices.get(
            speciality_id=offer.speciality_id,
            organization_id=offer.organization_id,
            internship=internship
        ).choice
        return str(choice)
    except (ObjectDoesNotExist, ValueError):
        return None


@reg.filter
def get_item(dictionary, key):
    val = dictionary.get(key)
    return val if val else ""
