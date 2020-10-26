import unittest

from controllers import (
    rating as rating_controller,
    neighborhood as controller,
    user as user_controller
)
from tests.mocks.mock_ratings import (
    correct_ratings,
    user,
    neighborhood as rating_neighborhood
)

from tests.mocks.mock_neighborhood import neighborhoods

from database import db
from database.models import Neighborhood


class TestNeighborhoodRating(unittest.TestCase):

    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(Neighborhood).all())

        # creates an user
        result, status = user_controller.create_user(user)
        self.assertEqual(result, "Created successfully!")
        self.assertEqual(status, 201)

        # create 3 neighborhoods
        for neighborhood in neighborhoods:
            result, status = controller.create_neighborhood(
                neighborhood)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        result, status = controller.get_all_neighborhoods()
        self.assertEqual(status, 200)
        for index in range(3):
            neighborhoods[index]['id_neighborhood'] = \
                result[index + self.db_len]['id_neighborhood']

        # create the ratings neighborhood
        result, status = controller.create_neighborhood(
                rating_neighborhood)
        self.assertEqual(result, "Created successfully!")
        self.assertEqual(status, 201)
        result, status = controller.get_all_neighborhoods()
        self.assertEqual(status, 200)
        rating_neighborhood['id_neighborhood'] = result[-1]['id_neighborhood']

        # creates 3 ratings
        for rating in correct_ratings:
            result, status = rating_controller.create_rating(
                rating, user['username'],
                rating_neighborhood['id_neighborhood']
            )
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        result, status = rating_controller.get_all_ratings()
        self.assertEqual(status, 200)
        for index in range(len(correct_ratings)):
            correct_ratings[index]['id_rating'] = \
                result[index + self.db_len]['id_rating']

    def tearDown(self):
        # deleting user
        result, status = user_controller.delete_user(user['username'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleted successfully!")

        # deleting all 3 ratings
        for rating in correct_ratings:
            result, status = rating_controller.delete_rating(
                rating['id_rating'],
            )
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")

        # deleting all 3 neighborhoods
        for neighborhood in neighborhoods:
            result, status = controller.delete_neighborhood(
                neighborhood['id_neighborhood'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")

        # deleting ratings neighborhood
        result, status = controller.delete_neighborhood(
                rating_neighborhood['id_neighborhood'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleted successfully!")

    def test_get_one_neighborhood(self):
        """
        Testing get one neighborhood with or without statistics
        """
        for neighborhood in neighborhoods:
            result, code = controller.get_one_neighborhood(
                                        neighborhood['id_neighborhood']
                                    )
            self.assertEqual(code, 200)
            self.assertEqual(result, neighborhood)

        result, code = controller.get_one_neighborhood(
                                    rating_neighborhood['id_neighborhood']
                                )
        self.assertEqual(code, 200)
        self.assertTrue('average' in result)
        self.assertTrue('lighting' in result)
        self.assertTrue('movement' in result)
        self.assertTrue('police' in result)
        self.assertAlmostEqual(result['average'], 2.7)
        self.assertEqual(result['lighting'], 2) 
        self.assertEqual(result['movement'], 3) 
        self.assertEqual(result['police'], 0)
        self.assertIsInstance(result, type(neighborhood))
