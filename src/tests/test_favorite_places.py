import unittest

from controllers import (
    favorite_places as controller,
    user as user_controller
)
from tests.mocks.mock_favorite_places import (
    users, places, place_without_name, invalid_places)

from database import db
from database.models import FavoritePlace


class TestFavoritePlaces(unittest.TestCase):

    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(FavoritePlace).all())
        self.qnt_places = len(places)

        # creates an users and generate the jwt token
        for user in users:
            result, status = user_controller.create_user(user)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        # creates places
        for place in places:
            result, status = controller.create_favorite_place(
                users[0]['username'], place)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

        result, status = controller.get_favorite_places(users[0]['username'])
        self.assertEqual(status, 200)
        for index, place in enumerate(places):
            place['id_place'] = \
                result[index]['id_place']

    def tearDown(self):
        # deleting all places
        for place in places:
            result, status = controller.delete_favorite_place(
                users[0]['username'], place['id_place'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")

        # deleting users
        for user in users:
            result, status = user_controller.delete_user(user['username'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")

        # asserting db len
        new_db_len = len(db.session.query(FavoritePlace).all())
        self.assertEqual(new_db_len, self.db_len)

    def test_create_favorite_place(self):
        """
        Testing create favorite places
        """
        new_db_len = len(db.session.query(FavoritePlace).all())
        self.assertEqual(new_db_len, self.db_len+self.qnt_places)

    def test_create_invalid_place(self):
        """
        Testing create invalid favorite places
        """
        result, status = controller.create_favorite_place(
                users[1]['username'], place_without_name)
        self.assertEqual(result, "Os seguintes campos estão faltando: name")
        self.assertEqual(status, 400)

        for place in invalid_places:
            result, status = controller.create_favorite_place(
                users[1]['username'], place)
            self.assertEqual(result, "Campo name com tamanho inválido!")
            self.assertEqual(status, 400)

    def test_get_favorite_place_from_user(self):
        """
        Testing get favorite places from one user
        """
        result, status = controller.get_favorite_places(users[0]['username'])
        self.assertEqual(status, 200)

        new_db_len = len(result)
        self.assertEqual(new_db_len, self.qnt_places)

        result, status = controller.get_favorite_places(users[1]['username'])
        self.assertEqual(status, 200)
        self.assertEqual(result, [])

    def test_delete_favorite_place(self):
        """
        Testing delete favorite place
        """
        result, status = controller.delete_favorite_place(users[0]['username'], -1)
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")

        result, status = controller.delete_favorite_place(
            users[1]['username'], places[0]['id_place'])
        self.assertEqual(status, 401)
        self.assertEqual(result, "Unauthorized to delete this place.")
