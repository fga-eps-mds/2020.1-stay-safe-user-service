import unittest
from controllers import user
from controllers.auth import authentication
from database import db
from database.models import User
from views.auth import make_auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.user = User(
        username= 'derfel.cadarn',
        email= 'derfel.baj@gmail.com',
        password= 'Tempestadegigante1',
        full_name= 'Derfel Cadarn'
        )
        user.create_user(user)

    def tearDown(self):
        user.delete_user(self.user.username)

    def test_authentication(self):
        result, status = authentication(
            {
            'username': self.user['username'],
            'password': 'Senhaerrada123'
            }
        )
        self.assertEqual(status, 401)
        self.assertEqual(result, 'Invalid password')

        result, status = authentication(
            {
            'username': self.user['username'],
            'password': self.user['password']
            }
        )
        self.assertEqual(status, 200)
        self.assertEqual(result, 'Validated successfully')

