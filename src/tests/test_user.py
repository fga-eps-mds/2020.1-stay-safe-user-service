import unittest

from controllers import user as controller
from tests.mock_users import (
    correct_users,
    wrong_users,
    correct_user_update
)
from database import db
from database.models import User

from settings import BCRYPT


class TestUser(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        self.db_len = len(db.session.query(User).all())
        self.qnt_users = len(correct_users)

        # tests whether valid users will be created
        for user in correct_users:
            result, status = controller.create_user(user)
            self.assertEqual(result, "Created successfully!")
            self.assertEqual(status, 201)

    def tearDown(self):
        for user in correct_users:  # deleting all users
            result, status = controller.delete_user(user['username'])
            self.assertEqual(status, 204)
            self.assertEqual(result, "Deleted successfully!")
        new_db_len = len(db.session.query(User).all())
        self.assertEqual(new_db_len, self.db_len)

    def test_create_user(self):
        """
        Testing create user
        """

        new_db_len = len(db.session.query(User).all())
        self.assertEqual(new_db_len, self.db_len+self.qnt_users)

        # tests whether invalid users will not be created
        for user in wrong_users:
            response, status = controller.create_user(user)
            self.assertEqual(status, 400)

    def test_get_all_users(self):
        """
        Testing get all users
        """
        result, status = controller.get_all_users()
        self.assertEqual(status, 200)
        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len + self.qnt_users)

    def test_get_one_user(self):
        """
        Testing get one users
        """
        for user in correct_users:
            result, status = controller.get_one_user(user['username'])
            self.assertEqual(status, 200)
            self.assertEqual(
                BCRYPT.check_password_hash(result['password'],
                                           user['password']),
                True
            )
            user_without_pswd = user.copy()
            del user_without_pswd['password']
            del result["password"]
            self.assertEqual(result, user_without_pswd)

        result, status = controller.get_one_user("unexisted#username")
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")

    def test_update_user(self):
        """
        Testing update user
        """
        user = correct_users[0]
        result, status = controller.update_user(
            user['username'],
            correct_user_update
        )

        self.assertEqual(status, 200)
        self.assertEqual(
            BCRYPT.check_password_hash(result['password'],
                                       correct_user_update['password']),
            True
        )

        correct_user_update['username'] = user['username']
        user_without_pswd = correct_user_update.copy()
        del user_without_pswd['password']
        del result["password"]
        self.assertEqual(result, user_without_pswd)

        for w_user in wrong_users:
            result, status = controller.update_user(
                user['username'],
                w_user
            )
            self.assertEqual(status, 400)

    def test_delete_user(self):
        """
        Testing delete users
        """
        result, status = controller.delete_user('unexisted#username')
        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")
