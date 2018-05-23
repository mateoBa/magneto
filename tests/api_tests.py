import json
import unittest
from unittest import mock

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

    @mock.patch('app.local_redis.LocalRedis.get')
    @mock.patch('app.local_redis.LocalRedis.set')
    def test_api_for_mutant(self, get_redis, set_redis):
        get_redis.return_value = []
        set_redis.return_value = []
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["ATGCGA", "CAGTGC", "TTATGT",
                                                    "AGAAGG", "CCCCTA", "TCACTG"]})
            self.assertEqual(result.status, '200 OK')

    @mock.patch('app.local_redis.LocalRedis.get')
    @mock.patch('app.local_redis.LocalRedis.set')
    def test_api_for_human(self, get_redis, set_redis):
        get_redis.return_value = []
        set_redis.return_value = []
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["ATGCGA", "CAGTGC", "TTATTT",
                                                    "AGACGG", "GCGTCA", "TCACTG"]})
            self.assertEqual(result.status, '403 FORBIDDEN')

    @mock.patch('app.local_redis.LocalRedis.get')
    def test_stats_api(self, get_redis):
        get_redis.return_value = []
        url = '/stats'
        with app.test_client() as client:
            result = client.get(url)
            data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status, '200 OK')
            self.assertEqual(data.get('count_mutant_dna'), 0)
            self.assertEqual(data.get('count_human_dna'), 0)
            self.assertEqual(data.get('ratio'), 0)

    @mock.patch('app.local_redis.LocalRedis.get')
    @mock.patch('app.local_redis.LocalRedis.set')
    def test_api_with_incorrect_data(self, get_redis, set_redis):
        get_redis.return_value = []
        set_redis.return_value = []
        url = '/mutant'
        with app.test_client() as client:
            result = client.post(url, json={'dna': ["XLS", "NZT", "SAR"]})
            self.assertEqual(result.status, '403 FORBIDDEN')


class IsMutantCase(unittest.TestCase):

    def test_is_mutant(self):
        data = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        self.assertEqual(is_mutant(data), True)

    def test_is_human(self):
        data = ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]
        self.assertEqual(is_mutant(data), False)
