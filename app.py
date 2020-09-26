from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api, output_json
from user_service import Accessor
from user_db import UserDB

app = Flask(__name__)
api = Api(app)

db_config = {"user": "postgres",
             "password": "postgres",
             "host": "127.0.0.1",
             "port": "5432",
             "db_name": "user_test"}


def init_db(db_config):
    db = UserDB(db_config)
    return db

class Ping(Resource):
    def get(self):
        return output_json({"ping": "pong"}, 200)

class CreateUser(Resource):
    def __init__(self, db):
        self.svc = Accessor(db)

    def post(self, name):
        resp = self.svc.create_user(name)
        return resp, 201

class GetUser(Resource):
    def __init__(self, db):
        self.svc = Accessor(db)

    def get(self, id):
        resp = self.svc.get_user(id)
        if resp["user_fetched"]:
            status = 200
        else:
            status = 404
        return resp, status

db = init_db(db_config)

api.add_resource(Ping, '/ping')
api.add_resource(CreateUser, '/user/create/<string:name>', resource_class_kwargs={"db": db})
api.add_resource(GetUser, '/user/get/<string:id>', resource_class_kwargs={"db": db})

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False,
            passthrough_errors=True, port=3000)
