import pickle

from app import redis_store


class LocalRedis(object):
    @classmethod
    def set(cls, key, data):
        li = redis_store.get(key)
        if li:
            li = pickle.loads(li)
            li.append(data)
        else:
            li = [data]

        redis_store.set(key, pickle.dumps(li))

    @classmethod
    def get(cls, key, default=None):
        val = redis_store.get(key)
        if val:
            return pickle.loads(val)
        return default
