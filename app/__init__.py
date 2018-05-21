from flask import Flask

app = Flask(__name__)

SEQUENCES_TO_FIND = 2


from app import api