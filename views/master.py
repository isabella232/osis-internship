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
from django.contrib.auth.decorators import login_required, permission_required
from base.views import layout
from internship.models import internship_master as mdl_internship_master
from internship.forms import form_search_master


@login_required
@permission_required('internship.can_access_internship', raise_exception=True)
def view_masters_list(request):
    specialities = mdl_internship_master.get_all_specialities()
    masters = []
    if request.method == "POST":
        form = form_search_master.SearchMasterForm(specialities, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            speciality = form.cleaned_data['speciality']
            organization = form.cleaned_data['organization']
            masters = mdl_internship_master.search(name=name, speciality=speciality, organization=organization)

    else:
        form = form_search_master.SearchMasterForm(specialities)

    return layout.render(request, "masters.html", {"masters": masters,
                                                   "search_form": form})
