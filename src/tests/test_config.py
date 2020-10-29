import unittest
from settings import load_configuration


class TestSettings(unittest.TestCase):
    def test_load_configuration(self):
        """
        Testing load configuration function
        """
        config = load_configuration()
        self.assertEqual(config['debug'], True)
        self.assertEqual(config['host'], '0.0.0.0')
        self.assertEqual(config['port'], 8083)
