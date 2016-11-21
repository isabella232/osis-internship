##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.test import TestCase
from admission.tests import data_for_tests
from performance.tests import data_for_tests as utility_data
from performance.models import student_performance as mdl_perf
from performance.queue import student_performance as queue_stud_perf
from django.core.exceptions import ObjectDoesNotExist
import json
from unittest.mock import patch


class TestQueueStudentPerformance(TestCase):
    def setUp(self):
        self.student_performance = data_for_tests.create_student_performance()
        self.offer_year = \
            data_for_tests.create_offer_year_with_academic_year(self.student_performance.offer_year.academic_year)
        self.json_points = utility_data.load_json_file("performance/tests/ressources/points2.json")
        self.json_points_2 = utility_data.load_json_file("performance/tests/ressources/points3.json")

    def test_save(self):
        student = self.student_performance.student
        offer_year = self.student_performance.offer_year
        stud_perf = queue_stud_perf.save(student, offer_year, self.json_points)

        self.student_performance.refresh_from_db()

        self.assertEqual(stud_perf, self.student_performance, "Object should be updated")

        other_student = data_for_tests.create_student_with_specific_registration_id("64641202")
        queue_stud_perf.save(other_student, offer_year, self.json_points)
        try:
            mdl_perf.StudentPerformance.objects.get(student=other_student, offer_year=offer_year)
        except ObjectDoesNotExist:
            self.fail("Object should be created")

    def test_generate_message(self):
        message = queue_stud_perf.generate_message(self.student_performance.student,
                                                   self.student_performance.offer_year)
        expected_message = json.dumps({"noma": "64641200", "sigle": "SINF2MS/G", "anac": "2016"})
        self.assertJSONEqual(message, expected_message, "Wrong message returned.")

    def test_extract_offer_year_from_json(self):
        offer_year = queue_stud_perf.extract_offer_year_from_json(json.loads(self.json_points))
        self.assertIsNotNone(offer_year, "Should return a valid offer year")
        self.assertEqual(offer_year.acronym, "SINF2MS/G", "Invalid acronym")
        self.assertEqual(offer_year.academic_year.year, 2016, "Invalid academic year")

    def test_extract_student_from_json(self):
        student = queue_stud_perf.extract_student_from_json(json.loads(self.json_points))
        self.assertIsNotNone(student, "Should return a valid student")
        self.assertEqual(student.registration_id, "64641200", "Invalid registration id")

    def test_callback(self):
        queue_stud_perf.callback(self.json_points.encode())
        self.student_performance.refresh_from_db()
        self.assertJSONEqual(json.dumps(self.student_performance.data), self.json_points, "Object should be updated")

        queue_stud_perf.callback(self.json_points_2.encode())

        try:
            mdl_perf.StudentPerformance.objects.get(student=self.student_performance.student,
                                                    offer_year=self.offer_year)
        except ObjectDoesNotExist:
            self.fail("Object should be created")

    @patch('frontoffice.queue.queue_listener.Client.call')
    def test_fetch_and_save(self, mock_client_call):
        mock_client_call.return_value = None
        obj = queue_stud_perf.fetch_and_save(self.student_performance.student,
                                             self.student_performance.offer_year)
        self.assertIsNone(obj, "Should return None")

        mock_client_call.return_value = self.json_points.encode()
        obj = queue_stud_perf.fetch_and_save(self.student_performance.student,
                                             self.student_performance.offer_year)
        self.assertIsNotNone(obj, "Should return a valid student performance object")
        self.assertJSONEqual(json.dumps(obj.data), self.json_points, "Incorrect student points json")
        self.assertEqual(self.student_performance.student, obj.student, "Incorrect student")
        self.assertEqual(self.student_performance.offer_year, obj.offer_year, "Incorrect offer year")
