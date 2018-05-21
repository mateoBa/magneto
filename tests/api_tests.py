import unittest

from app.api import is_mutant


class ApiTestCase(unittest.TestCase):

    pass


class IsMutantCase(unittest.TestCase):

    def test_is_mutant(self):
        data = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        self.assertEqual(is_mutant(data), True)

    def test_is_human(self):
        data = ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]
        self.assertEqual(is_mutant(data), False)
