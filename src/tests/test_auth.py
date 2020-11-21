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
        self.assertEqual(result, 'Senha inválida')

        result, status = authentication(
            {
                'username': self.user['username'],
                'password': self.user['password']
            }
        )
        self.assertEqual(status, 200)
        self.assertEqual(result['msg'], 'Login bem sucedido')

        result, status = authentication()
        self.assertEqual(status, 401)
        self.assertEqual(result, 'É necessário realizar o login')

    def test_authentication_without_password(self):
        result, status = authentication(
            {
                'username': self.user['username'],
                'password': None
            }
        )

        self.assertEqual(status, 401)
        self.assertEqual(result, "O nome de usuário e senha são obrigatórios")

    def test_authentication_without_username(self):
        result, status = authentication(
            {
                'username': None,
                'password': self.user['password']
            }
        )

        self.assertEqual(status, 401)
        self.assertEqual(result, "O nome de usuário e senha são obrigatórios")

    def test_authentication_with_inexisting_user(self):
        result, status = authentication(
            {
                'username': 'retriveu25',
                'password': self.user['password']
            }
        )

        self.assertEqual(status, 404)
        self.assertEqual(result, "Not Found!")
