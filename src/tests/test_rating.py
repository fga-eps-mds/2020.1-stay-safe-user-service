import unittest
import jwt
from settings import SECRET_KEY

from controllers import (
    rating as controller,
    neighborhood as neighborhood_controller,
    user as user_controller
)
from tests.mock_ratings import (
    correct_ratings,
    wrong_ratings,
    user,
    neighborhood,
    correct_update_rating
)

from database import db
from database.models import Rating, Neighborhood


class TestRating(unittest.TestCase):

    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(Rating).all())
        db_len_neighborhood = len(db.session.query(Neighborhood).all())

        # creates an user and generate the jwt token
        result, status = user_controller.create_user(user)
        self.assertEqual(result, "Created successfully!")
        self.assertEqual(status, 201)
        token = jwt.encode(
            {'username': user['username']}, SECRET_KEY, algorithm='HS256')

        self.header = {
            'Authorization': token
        }
        # create neighborhood
        result, status = neighborhood_controller.create_neighborhood(neighborhood, self.header)
        self.assertEqual(result, "Created successfully!")
        self.assertEqual(status, 201)

        result, status = neighborhood_controller.get_all_neighborhoods()
        self.assertEqual(status, 200)
        for index in range(1):
            neighborhood['id_neighborhood'] = \
                result[index + db_len_neighborhood]['id_neighborhood']

        # creates 3 ratings
        for rating in correct_ratings:
            result, status = controller.create_rating(
                rating, self.header, neighborhood['id_neighborhood'])
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        result, status = controller.get_all_ratings()
        self.assertEqual(status, 200)
        for index in range(3):
            correct_ratings[index]['id_rating'] = \
                result[index + self.db_len]['id_rating']


    def tearDown(self):
        # deleting all 3 ratings
        for rating in correct_ratings:
            result, status = controller.delete_rating(
                rating['id_rating'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")
        
        #deleting the neighborhood
        result, status = neighborhood_controller.delete_neighborhood(neighborhood['id_neighborhood'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleted successfully!")

        # deleting user
        result, status = user_controller.delete_user(user['username'])
        self.assertEqual(status, 204)
        self.assertEqual(result, "Deleted successfully!")

        # asserting db len
        new_db_len = len(db.session.query(Rating).all())
        self.assertEqual(new_db_len, self.db_len)

    def test_create_rating(self):
        """
        Testing create rating
        """
        new_db_len = len(db.session.query(Rating).all())
        self.assertEqual(new_db_len, self.db_len+3)

        # tests if invalid ratings will not be created
        for rating in wrong_ratings:
            response, status = controller.create_rating(
                rating, self.header, neighborhood['id_neighborhood'])
            self.assertEqual(status, 400)

    def test_get_all_ratings(self):
        """
        Testing get all ratings
        """
        result, status = controller.get_all_ratings()
        self.assertEqual(status, 200)

        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len + 3)

    def test_get_one_rating(self):
        """
        Testing get one rating
        """
        for rating in correct_ratings:
            result, status = controller.get_one_rating(
                rating['id_rating'])
            self.assertEqual(status, 200)
            self.assertEqual(
                result['rating_neighborhood'], rating['rating_neighborhood'])
            self.assertEqual(result['details'], rating['details'])

        result, status = controller.get_one_rating(-1)
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")

    def test_update_rating(self):
        """
        Testing update rating
        """
        rating = correct_ratings[0]
        result, status = controller.update_rating(
            rating['id_rating'],
            correct_update_rating
        )

        self.assertEqual(status, 200)
        self.assertEqual(
            result['rating_neighborhood'], 
            correct_update_rating['rating_neighborhood'])
        self.assertEqual(result['details'], correct_update_rating['details'])

        for wrong_rating in wrong_ratings:
            result, status = controller.update_rating(
                rating['id_rating'],
                wrong_rating
            )
            self.assertEqual(status, 400)

    def test_delete_rating(self):
        """
        Testing delete rating
        """
        result, status = controller.delete_rating(-1)
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")
