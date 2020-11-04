import unittest

from controllers import (
    occurrence as controller,
    user as user_controller
)
from tests.mocks.mock_occurrences import (
    correct_occurrences,
    wrong_occurrences,
    correct_occurrence_update,
    user
)

from database import db
from database.models import Occurrence


class TestOccurrence(unittest.TestCase):

    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(Occurrence).all())
        self.qnt_occurrence = len(correct_occurrences)

        # creates an user and generate the jwt token
        result, status = user_controller.create_user(user)
        self.assertEqual(result, "Created successfully!")
        self.assertEqual(status, 201)

        # creates occurrences
        for occurrence in correct_occurrences:
            result, status = controller.create_occurrence(
                user['username'], occurrence)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        result, status = controller.get_all_occurrences()
        self.assertEqual(status, 200)
        for index in range(len(correct_occurrences)):
            correct_occurrences[index]['id_occurrence'] = \
                result[index + self.db_len]['id_occurrence']

    def tearDown(self):
        # deleting user
        result, status = user_controller.delete_user(user['username'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleted successfully!")

        # deleting all occurrences
        for occurrence in correct_occurrences:
            result, status = controller.delete_occurrence(
                occurrence['id_occurrence'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")

        # asserting db len
        new_db_len = len(db.session.query(Occurrence).all())
        self.assertEqual(new_db_len, self.db_len)

    def test_create_occurrence(self):
        """
        Testing create occurrence
        """
        new_db_len = len(db.session.query(Occurrence).all())
        self.assertEqual(new_db_len, self.db_len+self.qnt_occurrence)

        # tests whether invalid occurrences will not be created
        for occurrence in wrong_occurrences:
            _, status = controller.create_occurrence(
                user['username'], occurrence)
            self.assertEqual(status, 400)

        # tries to create more than 5 ocurrences within 7 days
        result, status = controller.create_occurrence(
            user['username'], correct_occurrences[0])
        self.assertEqual(result,
                        "O limite de ocorrências cadastradas em 7 dias foi atingido.")
        self.assertEqual(status, 400)

    def test_get_all_occurrences(self):
        """
        Testing get all occurrences
        """
        result, status = controller.get_all_occurrences(user=user['username'])
        self.assertEqual(status, 200)

        new_db_len = len(correct_occurrences) + self.db_len
        self.assertEqual(new_db_len, self.db_len + self.qnt_occurrence)

        result, status = controller.get_all_occurrences(
            occurrence_type="Furto de Veículo"
        )
        self.assertEqual(status, 200)

        result, status = controller.get_all_occurrences(
            occurrence_type="Furto de Bicicleta"
        )
        self.assertEqual(status, 400)

        result, status = controller.get_all_occurrences()
        self.assertEqual(status, 200)

        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len + self.qnt_occurrence)

    def test_get_one_occurrence(self):
        """
        Testing get one occurrences
        """
        for occurrence in correct_occurrences:
            result, status = controller.get_one_occurrence(
                occurrence['id_occurrence'])
            self.assertEqual(status, 200)

            del result['register_date_time']
            occurrence_without_user = occurrence.copy()
            del occurrence_without_user['user']
            self.assertEqual(result, occurrence_without_user)

        result, status = controller.get_one_occurrence(-1)
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")

    def test_update_occurrence(self):
        """
        Testing update occurrence
        """
        occurrence = correct_occurrences[0]
        result, status = controller.update_occurrence(
            occurrence['id_occurrence'],
            correct_occurrence_update,
        )

        occurrence['police_report'] = True
        occurrence['occurrence_type'] = 'Roubo de Residência'
        del result['register_date_time']

        occurrence_without_user = occurrence.copy()
        del occurrence_without_user['user']
        self.assertEqual(status, 200)
        self.assertEqual(result, occurrence_without_user)

        for wrong_occurrence in wrong_occurrences:
            result, status = controller.update_occurrence(
                occurrence['id_occurrence'],
                wrong_occurrence,
            )
            self.assertEqual(status, 400)

    def test_delete_occurrence(self):
        """
        Testing delete occurrences
        """
        result, status = controller.delete_occurrence(-1)
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")

    def test_update_inexisting_occurrence(self):
        """
        Testing update inexisting occurrence
        """
        result, status = controller.update_occurrence(
            -2,
            correct_occurrence_update,
        )

        self.assertEqual(status, 404)
        self.assertEqual(result, 'Not Found!')

    def test_update_occurrence_from_another_user(self):
        """
        Testing update occurrence from another user
        """
        occurrence = correct_occurrences[0]
        result, status = controller.update_occurrence(
            occurrence['id_occurrence'],
            correct_occurrence_update,
            'aaaaaaaaaaaaa'
        )

        self.assertEqual(status, 403)
        self.assertTrue("You cannot edit another user's" in result)

    def test_delete_occurrence_from_another_user(self):
        """
        Testing delete occurrence from another user
        """
        occurrence = correct_occurrences[0]
        result, status = controller.delete_occurrence(
            occurrence['id_occurrence'],
            'aaaaaaaaaaaaa'
        )

        self.assertEqual(status, 403)
        self.assertTrue("You cannot delete another user's" in result)
