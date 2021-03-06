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
from database.models import Neighborhood, Rating


class TestNeighborhoodRating(unittest.TestCase):

    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(Neighborhood).all())
        self.rating_db_len = len(db.session.query(Rating).all())
        # the + 1 is the neighborhood on mock_ratings
        self.qnt_neighborhoods = len(neighborhoods) + 1

        # creates an user
        result, status = user_controller.create_user(user)
        self.assertEqual(result, "Criação bem-sucedida")
        self.assertEqual(status, 201)

        # create 3 neighborhoods
        for neighborhood in neighborhoods:
            result, status = controller.create_neighborhood(
                neighborhood)
            self.assertEqual(result, "Criação bem-sucedida")
            self.assertEqual(status, 201)

        result, status = controller.get_all_neighborhoods()
        self.assertEqual(status, 200)
        for index in range(3):
            neighborhoods[index]['id_neighborhood'] = \
                result[index + self.db_len]['id_neighborhood']

        # create the ratings neighborhood
        result, status = controller.create_neighborhood(
            rating_neighborhood)
        self.assertEqual(result, "Criação bem-sucedida")
        self.assertEqual(status, 201)
        result, status = controller.get_all_neighborhoods()
        self.assertEqual(status, 200)
        rating_neighborhood['id_neighborhood'] = result[-1]['id_neighborhood']

        # creates 3 ratings
        for rating in correct_ratings:
            rating = dict(filter(lambda x: x[0] != 'id_neighborhood'
                                 and x[0] != 'id_rating',
                                 rating.items()
                                 )
                          )
            result, status = rating_controller.create_rating(
                rating, user['username'],
                rating_neighborhood['id_neighborhood']
            )
            self.assertEqual(result, "Criação bem-sucedida")
            self.assertEqual(status, 201)

        result, status = rating_controller.get_all_ratings()
        self.assertEqual(status, 200)
        for index, correct_rating in enumerate(correct_ratings):
            correct_ratings[index]['id_rating'] = \
                result[index + self.rating_db_len]['id_rating']

    def tearDown(self):
        # deleting user
        result, status = user_controller.delete_user(user['username'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleção bem-sucedida")

        # deleting all 3 ratings
        for rating in correct_ratings:
            result, status = rating_controller.delete_rating(
                rating['id_rating'],
            )
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleção bem-sucedida")

        # deleting all 3 neighborhoods
        for neighborhood in neighborhoods:
            result, status = controller.delete_neighborhood(
                neighborhood['id_neighborhood'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleção bem-sucedida")

        # deleting ratings neighborhood
        result, status = controller.delete_neighborhood(
            rating_neighborhood['id_neighborhood'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleção bem-sucedida")

    def test_get_all_neighborhoods(self):
        """
        Testing get all neighborhoods
        """
        result, status = controller.get_all_neighborhoods(
            city=neighborhoods[0]['city'],
            state=neighborhoods[0]['state']
        )
        self.assertEqual(status, 200)

        new_db_len = len(result) + self.db_len
        self.assertEqual(new_db_len, self.db_len + self.qnt_neighborhoods)

        result, status = controller.get_all_neighborhoods(
            city=neighborhoods[0]['city']
        )
        self.assertEqual(status, 200)

        result, status = controller.get_all_neighborhoods(
            state=neighborhoods[0]['state']
        )
        self.assertEqual(status, 200)

        result, status = controller.get_all_neighborhoods()
        self.assertEqual(status, 200)

        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len + self.qnt_neighborhoods)

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
        self.assertTrue('statistics' in result)
        self.assertTrue('lighting' in result['statistics'])
        self.assertTrue('movement_of_people' in result['statistics'])
        self.assertTrue('police_rounds' in result['statistics'])
        self.assertAlmostEqual(result['statistics']['average'], 4)
        self.assertEqual(result['statistics']['lighting'], 1)
        self.assertEqual(result['statistics']['movement_of_people'], 2)
        self.assertEqual(result['statistics']['police_rounds'], 2)
        self.assertIsInstance(result, type(neighborhood))

    def test_get_one_inexisting_neighborhood(self):
        result, code = controller.get_one_neighborhood(-5)

        self.assertEqual(code, 404)
        self.assertEqual(result, "Not Found!")
