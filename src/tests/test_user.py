import unittest
import pytest 
from controllers import user as controller
from tests.users import users_correct, users_wrong, users_update_correct, users_update_wrong
from database import db
from database.models import User

from settings import logger

class TestUser(unittest.TestCase):
    def setUp(self):
        self.db_len = len(db.session.query(User).all()) # getting the db size before tests
        for user in users_correct: # creating 3 users for tests
            result, status = controller.create_user(user)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

    def tearDown(self):
        for user in users_correct: #deleting all 3 users
            result, status = controller.delete_user(user['username'])
            self.assertEqual(status, 204)
        new_db_len = len(db.session.query(User).all())
        self.assertEqual(self.db_len, new_db_len)

    def test_create_user(self):
        """
        Testing create user
        """
        for user in users_wrong: # assert that the db will not create unvalid users
            response, status = controller.create_user(user)
            self.assertEqual(status, 400)

    def test_get_all_users(self):
        """
        Testing get all users
        """
        result, status = controller.get_all_users()
        self.assertEqual(status, 200)
        new_db_len = len(result)
        self.assertEqual(self.db_len, new_db_len - 3)

    def test_get_one_user(self):
        """
        Testing get one users
        """
        for user in users_correct:
          load_user, status = controller.get_one_user(user['username'])
          self.assertEqual(status, 200)
          self.assertEqual(user, load_user)

    def test_update_user(self):
        """
        Testing update user
        """
        controller.update_user(users_correct[0]['username'], users_update_correct)
        controller.update_user(users_correct[0]['username'], users_update_wrong)

    def test_delete_user(self):
        """
        Testing delete users
        """
        result, status = controller.delete_user('unexisted_username')
        self.assertEqual(status, 404)
        