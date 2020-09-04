import unittest
import pytest 
from database.models 
from database import db


class User_test():
    def setUp(self):
        user = User(
                full_name = 'Mosoeusn Bararandir',
                username = 'Roiknebyu',
                email = 'anderson5458@uorak.com',
                password = 'mcX5EAuz'
        )
        db.insert_one(user)
        self.session.flush()

    def tearDown(self):
        self.session.flush()

    def test_create_user(self):
        """
        Testing create user
        """
        data = self.session.query(User).get(self.user.username)
        self.session.flush()
        assertEqual(data, self.user)

    def test_get_all_users():
        """
        Testing get all users
        """

    def test_get_one_user():
        """
        Testing get one users
        """
        data = self.session.query(User).get_one(User, 'Roiknebyu')
        self.assertEqual(data, self.user)

    def test_update_user():
        """
        Testing update user
        """

    def test_delete_user():
        """
        Testing delete users
        """
        user = self.session.query(User).filter(
            User.username == 'Roiknebyu'
        )

        response = self.session.delete(user)
        self.session.flush()
        self.assertIsNone(user)
        