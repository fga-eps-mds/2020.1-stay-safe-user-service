import unittest

from controllers import occurrence as controller
from tests.mock_occurrences import (
    correct_occurrences,
    wrong_occurrences,
    correct_occurrence_update
)
from database import db
from database.models import Occurrence

class TestOccurrence(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(Occurrence).all())

        # tests whether valid occurrences will be created
        header = {
         'Authorization': 'Bearer CVqOnmtK2fQasCGqsGzu0BlGsS3kmtejqTcwVDRw'
        }
        for occurrence in correct_occurrences:
            result, status = controller.create_occurrence(occurrence, header)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

    def tearDown(self):
        for occurrence in correct_occurrences:  # deleting all 3 occurrences
            result, status = controller.delete_occurrence(occurrence['id_occurrence'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")
        new_db_len = len(db.session.query(Occurrence).all())
        self.assertEqual(new_db_len, self.db_len)

    def test_create_occurrence(self):
        """
        Testing create occurrence
        """

        new_db_len = len(db.session.query(Occurrence).all())
        self.assertEqual(new_db_len, self.db_len+3)

        # tests whether invalid occurrences will not be created
        for occurrence in wrong_occurrences:
            response, status = controller.create_occurrence(occurrence)
            self.assertEqual(status, 400)

    # def test_get_all_occurrences(self):
    #     """
    #     Testing get all occurrences
    #     """
    #     result, status = controller.get_all_occurrences()
    #     self.assertEqual(status, 200)
    #     new_db_len = len(result)
    #     self.assertEqual(new_db_len, self.db_len + 3)

    # def test_get_one_occurrence(self):
    #     """
    #     Testing get one occurrences
    #     """
    #     for occurrence in correct_occurrences:
    #         result, status = controller.get_one_occurrence(occurrence['id_occurrence'])
    #         self.assertEqual(status, 200)
    #         self.assertEqual(result, occurrence)

    #     result, status = controller.get_one_occurrence("unexisted#occurrence")
    #     self.assertEqual(status, 404)
    #     self.assertEqual(result, "Not Found!")

    # def test_update_occurrence(self):
    #     """
    #     Testing update occurrence
    #     """
    #     occurrence = correct_occurrences[0]
    #     result, status = controller.update_occurrence(
    #         occurrence['occurrence'],
    #         correct_occurrence_update
    #     )

    #     self.assertEqual(status, 200)
    #     correct_occurrence_update['occurrence'] = occurrence['id_occurrence']
    #     self.assertEqual(result, correct_occurrence_update)

    #     for w_occurrence in wrong_occurrences:
    #         result, status = controller.update_occurrence(
    #             occurrence['occurrence'],
    #             w_occurrence
    #         )
    #         self.assertEqual(status, 400)

    # def test_delete_occurrence(self):
    #     """
    #     Testing delete occurrences
    #     """
    #     result, status = controller.delete_occurrence('unexisted#occurrence')
    #     self.assertEqual(status, 404)
    #     self.assertEqual(result, "Not Found!")
