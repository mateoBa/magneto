import json

from app import app, SEQUENCES_TO_FIND
from flask import request, Response

from app.local_redis import LocalRedis


def _find_result(values):
    count = 0
    for _, letter_value in values.items():
        for _, seq in letter_value.items():
            for _, val in seq.items():
                count += 1 if val >= 2 else 0
    return count


def _update_values(values, actual, sequence, index):
    if index in values[actual][sequence]:
        values[actual][sequence][index] += 1
    else:
        values[actual][sequence].update({index: 1})


def is_mutant(data):
    values = {'A': {'h': {}, 'v': {}, 'o_d': {}, 'o_u': {}}, 'T': {'h': {}, 'v': {}, 'o_d': {}, 'o_u': {}},
              'C': {'h': {}, 'v': {}, 'o_d': {}, 'o_u': {}}, 'G': {'h': {}, 'v': {}, 'o_d': {}, 'o_u': {}}}
    for i in range(1, len(data) - 1):
        for j in range(1, len(data) - 1):
            actual = data[i][j]
            if actual not in values:
                return None
            if actual == data[i + 1][j] and actual == data[i - 1][j]:
                _update_values(values, actual, 'v', j)
            if actual == data[i + 1][j + 1] and actual == data[i - 1][j - 1]:
                _update_values(values, actual, 'o_d', i - j)
            if actual == data[i - 1][j + 1] and actual == data[i + 1][j - 1]:
                _update_values(values, actual, 'o_u', i - j)
            if actual == data[i][j + 1] and actual == data[i][j - 1]:
                _update_values(values, actual, 'h', i)

    return _find_result(values) >= SEQUENCES_TO_FIND


@app.route('/mutant', methods=['POST'])
def is_mutant_api():
    data = request.get_json()
    if not data or (data and not data.get('dna')):
        return Response(status=204, mimetype='application/json')

    data = data.get('dna')
    # chequear si el arreglo es un cuadraro, sino devolver error
    rows = len(data)
    for r in data:
        if len(r) != rows:
            return Response('Error in data', status=400, mimetype='application/json')

    mutant_list = LocalRedis.get('mutant_list', [])
    if data in mutant_list:
        return Response('OK', status=200, mimetype='application/json')
    else:
        human_list = LocalRedis.get('human_list', [])
        if data in human_list:
            return Response('Forbidden', status=403, mimetype='application/json')

    if is_mutant(data):
        LocalRedis.set('mutant_list', data)
        return Response('OK', status=200, mimetype='application/json')
    LocalRedis.set('human_list', data)
    return Response('Forbidden', status=403, mimetype='application/json')


@app.route('/stats', methods=['GET'])
def stats():
    mutant_count = len(LocalRedis.get('mutant_list', []))
    human_count = len(LocalRedis.get('human_list', []))
    ratio = mutant_count/human_count if mutant_count and human_count else mutant_count+human_count

    data = {'count_mutant_dna': mutant_count, 'count_human_dna': human_count, 'ratio': ratio}
    return Response(json.dumps(data), status=200, mimetype='application/json')
