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
from internship import models as mdl_internship


START_PERIOD = 9
END_PERIOD = 12
MAX_PREFERENCE = 4
NUMBER_INTERNSHIPS = 4


class Solver:
    def __init__(self):
        self.offers = []
        self.students_dict = dict()

        self.offers_dict = dict()
        self.students_left_to_assign = []

    def initialize_f(self, filename):
        with open(filename) as file:
            number_offers, number_students = [int(x) for x in file.readline().split()]
            file.readline()

            for x in range(0, number_offers):
                self.__add_offer_from_line(file.readline())

            file.readline()

            for x in range(0, number_students):
                line = file.readline()
                self.__add_student_from_line(line)

    def __add_student_from_line(self, line):
        student = StudentWrapper.create_student(line)
        choice = Choice.create_choice(line)
        student.add_choice(choice)
        self.students_dict[student.student_id] = student
        self.students_left_to_assign.append(student)

    def __add_offer_from_line(self, line):
        offer = Offer.create_offer(line)
        key = (offer.organization_id, offer.speciality_id)
        self.offers_dict[key] = offer
        self.offers.append(offer)

    def get_number_offers(self):
        return len(self.offers_dict)

    def get_number_students(self):
        return len(self.students_dict)

    def add_student(self, student_obj):
        self.students_dict[student_obj.student_id] = student_obj

    def add_offer(self, offer_obj):
        self.offers_dict[(offer_obj.organization_id, offer_obj.speciality_id)] = offer_obj

    def get_offer(self, offer_organization_id, offer_speciality_id):
        return self.offers_dict.get((offer_organization_id, offer_speciality_id), None)

    def get_student(self, student_id):
        return self.students_dict.get(student_id, None)

    def solve(self):
        for preference in range(1, MAX_PREFERENCE + 1):
            for internship in range(1, NUMBER_INTERNSHIPS + 1):
                student_temp = []
                for student in self.students_left_to_assign:
                    if student.has_all_periods_assigned():
                        continue
                    choices = student.get_choices_for_preference(preference)
                    for choice in choices:
                        offer_key = (choice.organization_id, choice.speciality_id)
                        if offer_key not in self.offers_dict and not self.offers_dict[offer_key].has_place():
                            continue
                        offer = self.offers_dict[offer_key]
                        assigned = False
                        for period in offer.get_free_periods():
                            if student.has_period_unassigned(period):
                                student.assign(period, offer.offer_id)
                                assigned = True
                                break
                        if assigned:
                            break
                    student_temp.append(student)

                self.students_left_to_assign = student_temp

    def get_affectations(self):
        affectations = dict()
        for student_id, student_obj in self.students_dict.items():
            assignments = student_obj.get_assignments()
            affectations[student_id] = assignments


class Offer:
    def __init__(self, offer_id, organization_id, speciality_id, places):
        self.offer_id = offer_id
        self.organization_id = organization_id
        self.speciality_id = speciality_id
        self.places = dict()
        self.places_left = dict()
        self.__places_to_dict(places)

    def __places_to_dict(self, places):
        for index, value in enumerate(places):
            period = index + 1
            self.add_places(period, value)

    def get_period_places(self, period):
        return self.places_left.get(period, 0)

    @staticmethod
    def create_offer(line):
        line_in_ints = [int(x) for x in line.split()]
        offer_id = line_in_ints[0]
        organization_id = line_in_ints[1]
        speciality_id = line_in_ints[2]
        places = line_in_ints[3:]
        return Offer(offer_id, organization_id, speciality_id, places)

    def has_place(self, period):
        return self.get_period_places(period) > 0

    def occupy_place(self, period):
        self.places_left[period] -= 1

    def get_free_periods(self):
        periods = []
        for period in self.places_left.keys():
            if self.has_place(period):
                periods.append(period)
        return periods

    def add_places(self, period, places):
        self.places[period] = places
        self.places_left[period] = places


class StudentWrapper:
    def __init__(self, student):
        self.student = student
        self.assignments = dict()
        self.is_a_priority = False
        self.choices = []

        self._choices_by_preference = dict()
        self.cost = 0  # TODO compute cost

    def add_choice(self, choice):
        self.__add_by_preference(choice)
        self.__update_priority(choice)

    def __add_by_preference(self, choice):
        self.choices.append(choice)
        current_choices_for_preference = self._choices_by_preference.get(choice.choice, [])
        current_choices_for_preference.append(choice)
        self._choices_by_preference[choice.preference] = current_choices_for_preference

    def __update_priority(self, choice):
        if choice.priority:
            self.is_a_priority = True

    def assign(self, period, offer):
        self.assignments[period] = offer

    def has_all_periods_assigned(self):
        periods = [x for x in range(START_PERIOD, END_PERIOD+1)]
        for period in periods:
            if period not in self.assignments:
                return False
        return True

    def get_specialities_chosen(self):
        specialities = set()
        for choice in self.choices:
            specialities.add(choice.speciality)
        return list(specialities)

    def get_cost(self):
        return self.cost

    def get_choices_for_preference(self, preference):
        return self._choices_by_preference.get(preference, [])

    def has_period_unassigned(self, period):
        return False if period in self.assignments else True

    def get_assignments(self):
        return [(k, v) for (k, v) in self.assignments.items()]




