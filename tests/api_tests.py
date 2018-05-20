import unittest

from app.api import return_msg


class ApiTestCase(unittest.TestCase):
    def test_message(self):
        self.assertEqual(return_msg('desde test'), 'Hola Mundo desde test')
