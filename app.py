from flask import Flask, make_response, jsonify
from user_service import Accessor
from user_db import UserDB

app = Flask(__name__)

ERROR_INTERNAL_SERVER = "Internal Server Error"

db_config = {"user": "postgres",
             "password": "postgres",
             "host": "127.0.0.1",
             "port": "5432",
             "db_name": "user"}


def init(db_config):
    db = UserDB(db_config)
    svc = Accessor(db)
    return svc


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"ping": "pong"}), 200

