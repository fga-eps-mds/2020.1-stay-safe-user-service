import unittest
from controllers import user
from controllers.auth import authentication


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.user = {
            'full_name': 'Derfel Cadarn',
            'username': 'derfelcadarn2',
            'email': 'derfel.baj@gmail.com',
            'password': 'Tempestadegigante1'
        }
        user.create_user(self.user)

    def tearDown(self):
        user.delete_user(self.user['username'])

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
        self.assertEqual(result['msg'], 'Validated successfully')
