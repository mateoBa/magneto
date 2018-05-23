from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
redis_store = FlaskRedis(app)

SEQUENCES_TO_FIND = 2


from app import api