import json
import unittest
from app import app
from app.api import is_mutant


class ApiTestCase(unittest.TestCase):

    def test_empty_data(self):
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json=[])
            self.assertEqual(result.status, '204 NO CONTENT')
            result = client.post(url, json={'dna': []})
            self.assertEqual(result.status, '204 NO CONTENT')

    def test_matrix_malformed(self):
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["AT", "C"]})
            self.assertEqual(result.status, '400 BAD REQUEST')

    def test_api_for_mutant(self):
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["ATGCGA", "CAGTGC", "TTATGT",
                                                    "AGAAGG", "CCCCTA", "TCACTG"]})
            self.assertEqual(result.status, '200 OK')

    def test_api_for_human(self):
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["ATGCGA", "CAGTGC", "TTATTT",
                                                    "AGACGG", "GCGTCA", "TCACTG"]})
            self.assertEqual(result.status, '403 FORBIDDEN')


class IsMutantCase(unittest.TestCase):

    def test_is_mutant(self):
        data = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        self.assertEqual(is_mutant(data), True)

    def test_is_human(self):
        data = ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]
        self.assertEqual(is_mutant(data), False)
