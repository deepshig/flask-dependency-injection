import pytest
import sys
from flask.testing import FlaskClient
from flask import jsonify, Flask
sys.path.append('../')

from app import app, init  # NOQA
from user_service import Accessor  # NOQA

test_db_config = {"user": "postgres",
                  "password": "postgres",
                  "host": "127.0.0.1",
                  "port": "5432",
                  "db_name": "user_test"}


def test_ping():
    resp = app.test_client().get('/ping')
    assert resp.status_code == 200
    assert resp.data == b'{"ping":"pong"}\n'
