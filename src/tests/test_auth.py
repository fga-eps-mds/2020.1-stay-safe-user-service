import unittest
from controllers import user
from database import db
from database.models import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.db_len = len(db.session.query(User).all())

    def tearDown(self):
       