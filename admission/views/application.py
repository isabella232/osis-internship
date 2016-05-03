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
from admission import models as mdl
from django.shortcuts import render, get_object_or_404
from reference import models as mdl_reference

from admission.forms import FileForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from admission.views.common import home
from functools import cmp_to_key
import locale

ALERT_MANDATORY_FIELD = "Champ obligatoire"


def application_update(request, application_id):
    application = mdl.application.find_by_id(application_id)
    return render(request, "offer_selection.html",
                           {"offers":      None,
                            "offer":       application.offer_year,
                            "application": application})


def profile_confirmed(request):
    return render(request, "profile_confirmed.html")


def save_application_offer(request):
    if request.method == 'POST' and 'save' in request.POST:
        offer_year = None
        offer_year_id = request.POST.get('offer_year_id')

        application_id = request.POST.get('application_id')

        if application_id:
            application = get_object_or_404(mdl.application.Application, pk=application_id)
            secondary_education = mdl.secondary_education.find_by_person(application.person)
        else:
            application = mdl.application.Application()
            person_application = mdl.person.find_by_user(request.user)
            application.person = person_application
            secondary_education = mdl.secondary_education.SecondaryEducation()
            secondary_education.person = application.person

        if secondary_education.academic_year is None:
            secondary_education.academic_year = mdl.academic_year.current_academic_year()

        if offer_year_id:
            offer_year = mdl.offer_year.find_by_id(offer_year_id)
            if offer_year.grade_type:
                if offer_year.grade_type.grade == 'DOCTORATE':
                    application.doctorate = True
                else:
                    application.doctorate = False

        application.offer_year = offer_year
        application.save()
        # answer_question_
        for key, value in request.POST.items():
            if "txt_answer_question_" in key:
                answer = mdl.answer.Answer()
                answer.application = application
                answer.value = value
                # as it's txt_answer we know that it's there is only one option available,
                # (SHORT_INPUT_TEXT, LONG_INPUT_TEXT)
                option_id = key.replace("txt_answer_question_", "")
                answer.option = mdl.option.find_by_id(int(option_id))
                answer.save()
            else:
                if "txt_answer_radio_chck_optid_" in key:

                    # RADIO_BUTTON
                    if "on" == value:
                        answer = mdl.answer.Answer()
                        answer.application = application
                        option_id = key.replace("txt_answer_radio_chck_optid_", "")
                        option = mdl.option.find_by_id(int(option_id))
                        answer.option = option
                        answer.value = option.value
                        answer.save()
                else:
                    if "slt_question_" in key:
                        answer = mdl.answer.Answer()
                        answer.application = application
                        option = mdl.option.find_by_id(value)
                        answer.option = option
                        answer.value = option.value
                        answer.save()

        other_language_regime = mdl_reference.language.find_languages_by_recognized(False)
        recognized_languages = mdl_reference.language.find_languages_by_recognized(True)
        exam_types = mdl_reference.admission_exam_type.find_all_by_adhoc(False)
        local_language_exam_link = mdl.properties.find_by_key('PROFESSIONAL_EXAM_LINK')
        professional_exam_link = mdl.properties.find_by_key('LOCAL_LANGUAGE_EXAM_LINK')
        education_institutions = mdl_reference.education_institution.find_education_institution_by_adhoc(False)
        cities, postal_codes = find_cities_postalcodes(education_institutions)
        education_type_transition = mdl_reference.education_type.find_education_type_by_adhoc('TRANSITION', False)
        education_type_qualification = mdl_reference.education_type.find_education_type_by_adhoc('QUALIFICATION', False)
        return render(request, "diploma.html", {"application":                  application,
                                                "academic_years":               mdl.academic_year.find_academic_years(),
                                                "secondary_education":          secondary_education,
                                                "countries":                    mdl_reference.country.find_all(),
                                                "recognized_languages":         recognized_languages,
                                                "languages":                    other_language_regime,
                                                "exam_types":                   exam_types,
                                                "local_language_exam_link":     local_language_exam_link,
                                                "professional_exam_link":       professional_exam_link,
                                                "education_institutions":       education_institutions,
                                                "cities":                       cities,
                                                "postal_codes":                 postal_codes,
                                                "education_type_transition":    education_type_transition,
                                                "education_type_qualification": education_type_qualification})


def application_view(request, application_id):
    application = mdl.application.find_by_id(application_id)
    answers = mdl.answer.find_by_application(application_id)
    return render(request, "application.html",
                           {"application": application,
                            "answers": answers})


def diploma_save(request):
    next_step = False
    previous_step = False
    save_step = False
    validation_messages = {}
    academic_years = mdl.academic_year.find_academic_years()
    if request.POST:
        if 'bt_next_step_up' in request.POST or 'bt_next_step_down' in request.POST:
            next_step = True
        else:
            if 'bt_previous_step_up' in request.POST or 'bt_previous_step_down' in request.POST:
                previous_step = True
            else:
                if 'bt_save_up' in request.POST or 'bt_save_down' in request.POST:
                    save_step = True

    application = mdl.application.find_first_by_user(request.user) #???
    other_language_regime = mdl_reference.language.find_languages_by_recognized(False)
    recognized_languages = mdl_reference.language.find_languages_by_recognized(True)
    exam_types = mdl_reference.admission_exam_type.find_all_by_adhoc(False)
    person = mdl.person.find_by_user(request.user)
    secondary_education = mdl.secondary_education.find_by_person(person)

    local_language_exam_link = mdl.properties.find_by_key('PROFESSIONAL_EXAM_LINK')
    professional_exam_link = mdl.properties.find_by_key('LOCAL_LANGUAGE_EXAM_LINK')
    if secondary_education is None:
        secondary_education = mdl.secondary_education.SecondaryEducation()
        secondary_education.academic_year = mdl.academic_year.current_academic_year()
        secondary_education.person = application.person

    education_institutions = mdl_reference.education_institution.find_education_institution_by_adhoc(False)
    cities, postal_codes = find_cities_postalcodes(education_institutions)
    education_type_transition = mdl_reference.education_type.find_education_type_by_adhoc('TRANSITION', False)
    education_type_qualification = mdl_reference.education_type.find_education_type_by_adhoc('QUALIFICATION', False)
    if next_step or previous_step or save_step:
         # Check if all the necessary fields have been filled
        is_valid, validation_messages, secondary_education = validate_fields_form(request,
                                                                                  application.offer_year,
                                                                                  secondary_education,
                                                                                  next_step)
        if is_valid:
            secondary_education = populate_secondary_education(request, secondary_education)
            secondary_education.save()
            message_success = "Les données ont été enregistrées"
            if next_step:
                return render(request, "curriculum.html", {"application":         application,
                                                           "secondary_education": secondary_education,
                                                           "message_success":     message_success})
            else:
                if save_step:
                    countries = mdl_reference.country.find_all()
                    return render(request, "diploma.html", {"application":                  application,
                                                            "validation_messages":          validation_messages,
                                                            "academic_years":               academic_years,
                                                            "secondary_education":          secondary_education,
                                                            "countries":                    countries,
                                                            "recognized_languages":         recognized_languages,
                                                            "languages":                    other_language_regime,
                                                            "exam_types":                   exam_types,
                                                            'local_language_exam_link':     local_language_exam_link,
                                                            "professional_exam_link":       professional_exam_link,
                                                            "education_institutions":       education_institutions,
                                                            "cities":                       cities,
                                                            "postal_codes":                 postal_codes,
                                                            "education_type_transition":    education_type_transition,
                                                            "education_type_qualification": education_type_qualification,
                                                            "message_success":              message_success})
                else:
                    if previous_step:
                        return home(request)

        else:
            return render(request, "diploma.html", {"application":                  application,
                                                    "validation_messages":          validation_messages,
                                                    "academic_years":               academic_years,
                                                    "secondary_education":          secondary_education,
                                                    "countries":                    mdl_reference.country.find_all(),
                                                    "recognized_languages":         recognized_languages,
                                                    "languages":                    other_language_regime,
                                                    "exam_types":                   exam_types,
                                                    'local_language_exam_link':     local_language_exam_link,
                                                    "professional_exam_link":       professional_exam_link,
                                                    "education_institutions":       education_institutions,
                                                    "cities":                       cities,
                                                    "postal_codes":                 postal_codes,
                                                    "education_type_transition":    education_type_transition,
                                                    "education_type_qualification": education_type_qualification})
    else:
        return render(request, "diploma.html", {"application":                  application,
                                                "validation_messages":          validation_messages,
                                                "academic_years":               academic_years,
                                                "secondary_education":          secondary_education,
                                                "countries":                    mdl_reference.country.find_all(),
                                                "languages":                    other_language_regime,
                                                "recognized_languages":         recognized_languages,
                                                "exam_types":                   exam_types,
                                                'local_language_exam_link':     local_language_exam_link,
                                                "professional_exam_link":       professional_exam_link,
                                                "education_institutions":       education_institutions,
                                                "cities":                       cities,
                                                "postal_codes":                 postal_codes,
                                                "education_type_transition":    education_type_transition,
                                                "education_type_qualification": education_type_qualification})


def validate_fields_form(request, offer_yr, secondary_education, next_step):
    validation_messages = {}
    is_valid = True
    academic_year = None

    if request.POST.get('secondary_education_diploma'):
        if request.POST.get('secondary_education_diploma') == 'true':
            # secondary education diploma
            secondary_education.secondary_education_diploma = True

            if request.POST.get('academic_year') is None:
                validation_messages['academic_year'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                academic_year = mdl.academic_year.find_by_id(int(request.POST.get('academic_year')))
                secondary_education.academic_year = academic_year
            if request.POST.get('rdb_belgian_foreign') is None:
                validation_messages['rdb_belgian_foreign'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                if request.POST.get('rdb_belgian_foreign') == 'true':
                    secondary_education.national = True
                    # Belgian diploma
                    if request.POST.get('result') is None:
                        validation_messages['result'] = ALERT_MANDATORY_FIELD
                        is_valid = False
                    else:
                        secondary_education.result = request.POST.get('result')
                    if request.POST.get('rdb_belgian_community') is None:
                        validation_messages['rdb_belgian_community'] = ALERT_MANDATORY_FIELD
                        is_valid = False
                    else:
                        secondary_education.national_community = request.POST.get('rdb_belgian_community')
                        if request.POST.get('rdb_belgian_community') == 'FRENCH':
                            # diploma of the French community
                            if academic_year.year < 1994:
                                if request.POST.get('daes') is None:
                                    validation_messages['daes'] = ALERT_MANDATORY_FIELD
                                    is_valid = False
                            if request.POST.get('chb_other_education') == 'on':
                                if request.POST.get('other_education_type') is None:
                                    validation_messages['pnl_teaching_type'] = "Il faut préciser un type " \
                                                                               "d'enseignement autre"
                                    is_valid = False
                                else:
                                    new_education_type = mdl_reference.education_type.EducationType()
                                    new_education_type.adhoc = True
                                    new_education_type.name = request.POST.get('other_education_type')
                                    new_education_type.type = 'ANOTHER'
                                    secondary_education.education_type = new_education_type

                        else:
                            if request.POST.get('rdb_belgian_community') == 'DUTCH':
                                # diploma of the Dutch community
                                if academic_year.year < 1992:
                                    if request.POST.get('daes') is None:
                                        validation_messages['daes'] = ALERT_MANDATORY_FIELD
                                        is_valid = False

                    if request.POST.get('school_belgian_community') == 'FRENCH':
                        # Belgian school
                        if request.POST.get('rdb_education_transition_type') is None \
                                and request.POST.get('rdb_education_technic_type') \
                                and request.POST.get('other_education'):
                            validation_messages['pnl_teaching_type'] = "Il faut préciser un type d'enseignement"
                            is_valid = False

                        else:
                            if request.POST.get('rdb_education_transition_type'):
                                secondary_education.education_type = mdl_reference.education_type\
                                    .find_by_id(int(request.POST.get('rdb_education_transition_type')))
                            if request.POST.get('rdb_education_technic_type'):
                                secondary_education.education_type = mdl_reference.education_type\
                                    .find_by_id(int(request.POST.get('rdb_education_technic_type')))

                    if academic_year.year < 1994:
                        if request.POST.get('path_repetition') is None:
                            validation_messages['path_repetition'] = ALERT_MANDATORY_FIELD
                            is_valid = False
                        if request.POST.get('path_reorientation') is None:
                            validation_messages['path_reorientation'] = ALERT_MANDATORY_FIELD
                            is_valid = False

                else:
                    if request.POST.get('rdb_belgian_foreign') == 'false':
                        if request.POST.get('result') is None:
                            validation_messages['result'] = ALERT_MANDATORY_FIELD
                            is_valid = False
                        else:
                            secondary_education.result = request.POST.get('result')
                        secondary_education.national = False
                        # Foreign diploma
                        if request.POST.get('international_diploma') is None:
                            validation_messages['international_diploma'] = "Il faut préciser le diplôme obtenu"
                            is_valid = False
                        else:
                            secondary_education.international_diploma = request.POST.get('international_diploma')
                            print('ici', secondary_education.international_diploma)
                            if secondary_education.international_diploma == 'INTERNATIONAL':
                                print(request.POST.get('international_equivalence') )
                                if request.POST.get('international_equivalence') is None:
                                    validation_messages['international_equivalence'] = ALERT_MANDATORY_FIELD
                                    is_valid = False
                                else:
                                    secondary_education.international_equivalence = request.POST.get('international_equivalence')
                            else:
                                secondary_education.international_equivalence = None
                        if request.POST.get('other_language_regime') == 'on':
                            if request.POST.get('other_language_diploma') == "-":
                                validation_messages['language_regime'] = "Il faut préciser un régime linguistique \
                                                                          de type autre"
                                is_valid = False
                        else:
                            if request.POST.get('international_diploma_language') == "-":
                                validation_messages['language_regime'] = "Il faut préciser un régime linguistique"
                                is_valid = False

                if (request.POST.get('school') is None or request.POST.get('school') == "-")\
                    and ((request.POST.get('CESS_other_school_name') is None\
                          or (len(request.POST.get('CESS_other_school_name')) == 0))\
                         and (request.POST.get('CESS_other_school_city') is None\
                              or len(request.POST.get('CESS_other_school_city')) == 0)\
                         and (request.POST.get('CESS_other_school_postal_code') is None\
                              or len(request.POST.get('CESS_other_school_postal_code')) == 0)):
                    validation_messages['school'] = "Il faut préciser un établissement scolaire"
                    is_valid = False
                    # reset institution fields
                    secondary_education.national_institution = mdl_reference.education_institution.EducationInstitution()
                    secondary_education.national_institution.name = ""
                    secondary_education.national_institution.city = ""
                    secondary_education.national_institution.postal_code = ""
                    secondary_education.national_institution.adhoc = False
                else:
                    if request.POST.get('other_school') == "on":
                        if request.POST.get('school_belgian_community') is None:
                            validation_messages['school'] = "Il faut préciser un type de communauté " \
                                                            "pour l'établissement"
                            is_valid = False
                            national_institution = mdl_reference.education_institution.EducationInstitution()
                            national_institution.adhoc = True
                            national_institution.name = request.POST.get('CESS_other_school_name')
                            national_institution.city = request.POST.get('CESS_other_school_city')
                            national_institution.postal_code = request.POST.get('CESS_other_school_postal_code')

                            if request.POST.get('school_belgian_community'):
                                national_institution.national_community = request.POST\
                                    .get('school_belgian_community')
                            secondary_education.national_institution = national_institution

                    else:
                        if request.POST.get('school') \
                                and request.POST.get('school') != "-" \
                                and request.POST.get('school').isnumeric():
                            national_institution = mdl_reference.education_institution\
                                .find_by_id(int(request.POST.get('school')))
                            secondary_education.national_institution = national_institution
        else:
            is_valid, validation_messages, secondary_education = validate_admission_exam(request,
                                                                                         is_valid,
                                                                                         validation_messages,
                                                                                         secondary_education,
                                                                                         offer_yr)
    else:
        validation_messages['secondary_education_diploma'] = ALERT_MANDATORY_FIELD
        is_valid = False

    is_valid, validation_messages, secondary_education = validate_professional_exam(request,
                                                                                    is_valid,
                                                                                    validation_messages,
                                                                                    secondary_education)
    is_valid, validation_messages, secondary_education = validate_local_language_exam(request,
                                                                                      is_valid,
                                                                                      validation_messages,
                                                                                      secondary_education)

    if next_step is True \
            and request.POST.get('secondary_education_diploma') == 'false' \
            and request.POST.get('admission_exam') == 'false' \
            and request.POST.get('professional_exam') == 'false':
        validation_messages['final'] = "Impossible de passer à l'étape suivante. Il faut avoir \
                                            répondu 'Oui' pour les études secondaires ou \
                                            pour l'examen d'admission ou encore pour les expériences \
                                            professionnelles."
        is_valid = False

    return is_valid, validation_messages, secondary_education


def curriculum_read(request, application_id):
    application = mdl.application.find_by_id(application_id)
    return render(request, "curriculum.html", {"application": application})


def curriculum_save(request, application_id):

    exam_types = mdl_reference.admission_exam_type.find_all_by_adhoc(False)

    local_language_exam_link = mdl.properties.find_by_key('PROFESSIONAL_EXAM_LINK')
    professional_exam_link = mdl.properties.find_by_key('LOCAL_LANGUAGE_EXAM_LINK')

    application = mdl.application.find_by_id(application_id)
    other_language_regime = mdl_reference.language.find_languages_by_recognized(False)
    recognized_languages = mdl_reference.language.find_languages_by_recognized(True)

    secondary_education = mdl.secondary_education.find_by_person(application.person)
    education_institutions = mdl_reference.education_institution.find_education_institution_by_adhoc(False)
    cities, postal_codes = find_cities_postalcodes(education_institutions)
    education_type_transition = mdl_reference.education_type.find_education_type_by_adhoc('TRANSITION', False)
    education_type_qualification = mdl_reference.education_type.find_education_type_by_adhoc('QUALIFICATION', False)
    return render(request, "diploma.html", {"application":                  application,
                                            "academic_years":               mdl.academic_year.find_academic_years(),
                                            "secondary_education":          secondary_education,
                                            "countries":                    mdl_reference.country.find_all(),
                                            "recognized_languages":         recognized_languages,
                                            "languages":                    other_language_regime,
                                            "exam_types":                   exam_types,
                                            'local_language_exam_link':     local_language_exam_link,
                                            "professional_exam_link":       professional_exam_link,
                                            "education_institutions":       education_institutions,
                                            "cities":                       cities,
                                            "postal_codes":                 postal_codes,
                                            "education_type_transition":    education_type_transition,
                                            "education_type_qualification": education_type_qualification})


def upload_file(request, secondary_education_id):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            # faut sauver le fichier dans le model et sur disk?
            print('file name:', file_name)
    return HttpResponseRedirect(reverse('diploma', args=[ ]))


def find_cities_postalcodes(education_institutions):
    cities = []
    postal_codes = []
    for education_institution in education_institutions:
        if education_institution.city not in cities:
            cities.append(education_institution.city)
        if education_institution.postal_code not in postal_codes:
            postal_codes.append(education_institution.postal_code)
    return sorted(cities, key=cmp_to_key(locale.strcoll)), sorted(postal_codes, key=cmp_to_key(locale.strcoll))


def populate_secondary_education(request, secondary_education):
    #belgian
    secondary_education.secondary_education_diploma = None
    if request.POST.get('secondary_education_diploma'):
        if request.POST.get('secondary_education_diploma') == 'true':
            secondary_education.secondary_education_diploma = True
        else:
            secondary_education.secondary_education_diploma = False

    secondary_education.academic_year = None
    if request.POST.get('academic_year'):
        academic_year = mdl.academic_year.find_by_id(int(request.POST.get('academic_year')))
        secondary_education.academic_year = academic_year
    secondary_education.national = None
    secondary_education.result = None
    if request.POST.get('rdb_belgian_foreign'):
        if request.POST.get('rdb_belgian_foreign') == 'true':
            secondary_education.national = True
            secondary_education.result = request.POST.get('result')
        else:
            secondary_education.national = False
    secondary_education.national_community = None
    if request.POST.get('rdb_belgian_community'):
        secondary_education.national_community = request.POST.get('rdb_belgian_community')

    secondary_education.national_institution = None
    if request.POST.get('other_school') == "on":
        existing_education_institution = mdl_reference.education_institution\
                                .find_by_name_city_postal_code(request.POST.get('CESS_other_school_name'),\
                                                               request.POST.get('CESS_other_school_city'),\
                                                               request.POST.get('CESS_other_school_postal_code'),
                                                               request.POST.get('school_belgian_community'))
        if existing_education_institution:
            secondary_education.national_institution = existing_education_institution
        else:
            new_education_institution = mdl_reference.education_institution.EducationInstitution()
            new_education_institution.name = request.POST.get('CESS_other_school_name')
            new_education_institution.city = request.POST.get('CESS_other_school_city')
            new_education_institution.postal_code = request.POST.get('CESS_other_school_postal_code')
            new_education_institution.institution_type="SECONDARY"
            new_education_institution.national_community = request.POST.get('school_belgian_community')
            new_education_institution.adhoc = True
            new_education_institution.save()
            secondary_education.national_institution = new_education_institution
    else:
        if request.POST.get('school'):
            national_institution = mdl_reference.education_institution.find_by_id(int(request.POST.get('school')))
            secondary_education.national_institution = national_institution

    secondary_education.education_type = None
    if request.POST.get('chb_other_education') == 'on':
        existing_education_type = mdl_reference.education_type.find_by_name(request.POST.get('other_education_type'))
        if existing_education_type:
            secondary_education.education_type = existing_education_type
        else:
            new_education_type = mdl_reference.education_type.EducationType()
            new_education_type.adhoc = True
            new_education_type.name = request.POST.get('other_education_type')
            new_education_type.type = 'ANOTHER'
            new_education_type.save()
            secondary_education.education_type = new_education_type
    else:
        if request.POST.get('rdb_education_transition_type'):
            secondary_education.education_type = mdl_reference.education_type.find_by_id(int(request.POST.get('rdb_education_transition_type')))
        if request.POST.get('rdb_education_technic_type'):
            secondary_education.education_type = mdl_reference.education_type.find_by_id(int(request.POST.get('rdb_education_technic_type')))
    # ???Je en comprends pas pq ceci donne une erreur
    #secondary_education.daes = None
    secondary_education.daes = False
    if request.POST.get('daes'):
        if request.POST.get('daes') == 'true':
            secondary_education.daes = True
        else:
            if request.POST.get('daes') == 'false':
                secondary_education.daes = False

    secondary_education.path_repetition = None
    if request.POST.get('path_repetition'):
        if request.POST.get('path_repetition') == 'true':
            secondary_education.path_repetition = True
        else:
            if request.POST.get('path_repetition') == 'false':
                secondary_education.path_repetition = False

    secondary_education.path_reorientation = None
    if request.POST.get('path_reorientation'):
        if request.POST.get('path_reorientation') == 'true':
            secondary_education.path_reorientation = True
        else:
            if request.POST.get('path_reorientation') == 'false':
                secondary_education.path_reorientation = False
    #international_diploma
    secondary_education.international_diploma = None
    secondary_education.international_diploma_country = None
    secondary_education.international_diploma_language = None
    secondary_education.international_equivalence = None
    if secondary_education.secondary_education_diploma is True and secondary_education.national is False:
        secondary_education.international_diploma = request.POST.get('international_diploma')
        secondary_education.international_diploma_country = request.POST.get('international_diploma_country')
        if request.POST.get('other_language_regime') \
            and request.POST.get('other_language_regime') == "on" \
            and request.POST.get('other_language_regime') != "-":
            secondary_education.international_diploma_language = mdl_reference.language\
                .find_by_id(int(request.POST.get('other_international_diploma_language')))
        else:
            if request.POST.get('international_diploma_language') \
                    and request.POST.get('international_diploma_language') != "-":
                secondary_education.international_diploma_language = mdl_reference.language\
                    .find_by_id(int(request.POST.get('international_diploma_language')))

        secondary_education.international_equivalence = request.POST.get('international_equivalence')

        secondary_education.result = request.POST.get('foreign_result')

    #admission_exam
    secondary_education.admission_exam = None
    secondary_education.admission_exam_date = None
    secondary_education.admission_exam_institution = None
    secondary_education.admission_exam_type = None
    secondary_education.admission_exam_result = None
    if request.POST.get('admission_exam'):
        if request.POST.get('admission_exam') == 'true':
            secondary_education.admission_exam = True
            if request.POST.get('admission_exam_date'):
                secondary_education.admission_exam_date = datetime\
                    .strptime(request.POST.get('admission_exam_date'), '%d/%m/%Y')
            if request.POST.get('admission_exam_institution'):
                secondary_education.admission_exam_institution = request.POST.get('admission_exam_institution')
            if request.POST.get('admission_exam_type_other') \
                    and len(request.POST.get('admission_exam_type_other').strip()) > 0:
                existing_admission_exam_type = mdl_reference.admission_exam_type\
                    .find_by_name(request.POST.get('admission_exam_type_other'))
                if existing_admission_exam_type:
                    secondary_education.admission_exam_type = existing_admission_exam_type
                else:
                    new_admission_exam_type = mdl_reference.admission_exam_type.AdmissionExamType()
                    new_admission_exam_type.adhoc = True
                    new_admission_exam_type.name = request.POST.get('admission_exam_type_other')
                    new_admission_exam_type.save()
                    secondary_education.admission_exam_type = new_admission_exam_type
            else:
                if request.POST.get('admission_exam_type'):
                    secondary_education.admission_exam_type = mdl_reference.admission_exam_type\
                        .find_by_name(request.POST.get('admission_exam_type'))

            secondary_education.admission_exam_result = request.POST.get('admission_exam_result')
        else:
            if request.POST.get('admission_exam') == 'false':
                secondary_education.admission_exam = False

    secondary_education.professional_exam = None
    secondary_education.professional_exam_date = None
    secondary_education.professional_exam_institution = None
    secondary_education.professional_exam_result = None
    if request.POST.get('professional_exam'):
        if request.POST.get('professional_exam') == 'true':
            secondary_education.professional_exam = True
            secondary_education.professional_exam_date = datetime\
                .strptime(request.POST.get('professional_exam_date'), '%d/%m/%Y')
            secondary_education.professional_exam_institution = request.POST.get('professional_exam_institution')
            secondary_education.professional_exam_result = request.POST.get('professional_exam_result')
        else:
            if request.POST.get('professional_exam') == 'false':
                secondary_education.professional_exam = False

    secondary_education.local_language_exam = None
    secondary_education.local_language_exam_date = None
    secondary_education.local_language_exam_institution = None
    secondary_education.local_language_exam_result = None
    if request.POST.get('local_language_exam'):
        if request.POST.get('local_language_exam') == 'true':
            secondary_education.local_language_exam = True
            secondary_education.local_language_exam_date = datetime\
                .strptime(request.POST.get('local_language_exam_date'), '%d/%m/%Y')
            secondary_education.local_language_exam_institution = request.POST.get('local_language_exam_institution')
            secondary_education.local_language_exam_result = request.POST.get('local_language_exam_result')
        else:
            if request.POST.get('local_language_exam') == 'false':
                secondary_education.local_language_exam = False

    return secondary_education


def diploma_update(request):
    application = mdl.application.find_first_by_user(request.user)
    person = mdl.person.find_by_user(request.user)
    other_language_regime = mdl_reference.language.find_languages_by_recognized(False)
    recognized_languages = mdl_reference.language.find_languages_by_recognized(True)
    exam_types = mdl_reference.admission_exam_type.find_all_by_adhoc(False)
    secondary_education = mdl.secondary_education.find_by_person(person)
    education_institutions = mdl_reference.education_institution.find_education_institution_by_adhoc(False)
    cities, postal_codes = find_cities_postalcodes(education_institutions)
    education_type_transition = mdl_reference.education_type.find_education_type_by_adhoc('TRANSITION', False)
    education_type_qualification = mdl_reference.education_type.find_education_type_by_adhoc('QUALIFICATION', False)
    local_language_exam_link = mdl.properties.find_by_key('PROFESSIONAL_EXAM_LINK')
    professional_exam_link = mdl.properties.find_by_key('LOCAL_LANGUAGE_EXAM_LINK')
    countries = mdl_reference.country.find_all()
    academic_years = mdl.academic_year.find_academic_years()
    return render(request, "diploma.html", {"application":                  application,
                                            "academic_years":               academic_years,
                                            "secondary_education":          secondary_education,
                                            "countries":                    countries,
                                            "recognized_languages":         recognized_languages,
                                            "languages":                    other_language_regime,
                                            "exam_types":                   exam_types,
                                            'local_language_exam_link':     local_language_exam_link,
                                            "professional_exam_link":       professional_exam_link,
                                            "education_institutions":       education_institutions,
                                            "cities":                       cities,
                                            "postal_codes":                 postal_codes,
                                            "education_type_transition":    education_type_transition,
                                            "education_type_qualification": education_type_qualification})


def validate_professional_exam(request,is_valid, validation_messages, secondary_education):
    if request.POST.get('professional_exam') is None:
        validation_messages['professional_exam'] = ALERT_MANDATORY_FIELD
        is_valid = False
    else:
        if request.POST.get('professional_exam') == 'true':
            secondary_education.professional_exam = True
            if request.POST.get('professional_exam_date') is None \
                    or len(request.POST.get('professional_exam_date').strip()) == 0:
                validation_messages['professional_exam_date'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                try:
                    secondary_education.professional_exam_date = datetime\
                        .strptime(request.POST.get('professional_exam_date'), '%d/%m/%Y')
                except:
                    validation_messages['professional_exam_date'] = "La date (%s) semble erronée" % \
                                                                    request.POST.get('professional_exam_date')
                    is_valid = False
                    secondary_education.professional_exam_date = None

            if request.POST.get('professional_exam_institution') is None \
                    or len(request.POST.get('professional_exam_institution').strip()) == 0:
                validation_messages['professional_exam_institution'] = ALERT_MANDATORY_FIELD
                is_valid = False
                secondary_education.professional_exam_institution = None
            else:
                secondary_education.professional_exam_institution = request.POST.get('professional_exam_institution')
            if request.POST.get('professional_exam_result') is None:
                validation_messages['professional_exam_result'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                secondary_education.professional_exam_result = request.POST.get('professional_exam_result')
        else:
            if request.POST.get('professional_exam') == 'false':
                secondary_education.professional_exam = False
    return is_valid, validation_messages, secondary_education


def validate_local_language_exam(request,is_valid, validation_messages, secondary_education):
    if request.POST.get('local_language_exam') is None:
        validation_messages['local_language_exam'] = "Il faut répondre oui ou non"
        is_valid = False
    else:
        if request.POST.get('local_language_exam') == 'true':
            secondary_education.local_language_exam = True

            if request.POST.get('local_language_exam_date') is None \
                    or len(request.POST.get('local_language_exam_date').strip()) == 0:
                validation_messages['local_language_exam_date'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                try:
                    secondary_education.local_language_exam_date = datetime\
                        .strptime(request.POST.get('local_language_exam_date'), '%d/%m/%Y')
                except:
                    validation_messages['local_language_exam_date'] = "La date (%s) semble erronée" % \
                                                                    request.POST.get('local_language_exam_date')
                    is_valid = False
                    secondary_education.local_language_exam_date = None

            if request.POST.get('local_language_exam_institution') is None \
                    or len(request.POST.get('local_language_exam_institution').strip()) == 0:
                validation_messages['local_language_exam_institution'] = ALERT_MANDATORY_FIELD
                is_valid = False
                secondary_education.local_language_exam_institution = None
            else:
                secondary_education.local_language_exam_institution = request.POST.get('local_language_exam_institution')
            if request.POST.get('local_language_exam_result') is None:
                validation_messages['local_language_exam_result'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                secondary_education.local_language_exam_result = request.POST.get('local_language_exam_result')
        else:
            secondary_education.local_language_exam = False
    return is_valid, validation_messages, secondary_education


def validate_admission_exam(request,is_valid, validation_messages, secondary_education, offer_yr):
    if request.POST.get('admission_exam') is None:
        validation_messages['admission_exam'] = ALERT_MANDATORY_FIELD
        is_valid = False
    else:
        if request.POST.get('admission_exam') == 'true':
            secondary_education.admission_exam = True

            if request.POST.get('admission_exam_date') is None:
                validation_messages['admission_exam_date'] = ALERT_MANDATORY_FIELD
                is_valid = False
            if request.POST.get('admission_exam_institution') is None \
                    or len(request.POST.get('admission_exam_institution').strip()) == 0:
                validation_messages['admission_exam_institution'] = ALERT_MANDATORY_FIELD
                is_valid = False
            if request.POST.get('admission_exam_type') is None \
                    and (request.POST.get('admission_exam_type_other') is None
                         or len(request.POST.get('admission_exam_type_other').strip()) == 0):
                validation_messages['admission_exam_type'] = ALERT_MANDATORY_FIELD
                is_valid = False
            else:
                #???
                if mdl.offer_year.is_engineering(offer_yr) is True:
                    if request.POST.get('admission_exam_type') != 'FIRST_CYCLE_CIVIL_ENGINEER':
                        validation_messages['admission_exam_type'] = "Pour les offres 'Ingenieur Civil' " \
                                                                     "(FSA1BA et ARCH1BA), l'examen spécial " \
                                                                     "d'admission aux études universitaires " \
                                                                     "de 1er cycle de l'ingénieur (ingénieur " \
                                                                     "civil) est obliqatoire"
                        is_valid = False

                if request.POST.get('admission_exam_type') == 'OTHER_EXAM':
                    if request.POST.get('admission_exam_type_other') is None \
                            or len(request.POST.get('admission_exam_type_other').strip()) == 0:
                        validation_messages['admission_exam_type'] = "Pour autre examen il faut préciser"
                        is_valid = False
            if request.POST.get('admission_exam_result') is None:
                validation_messages['admission_exam_result'] = ALERT_MANDATORY_FIELD
                is_valid = False
        else:
            if request.POST.get('admission_exam') == 'false':
                secondary_education.admission_exam = False

    return is_valid, validation_messages, secondary_education
