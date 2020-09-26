import pytest
import sys
from flask.testing import FlaskClient
from flask import jsonify, Flask
sys.path.append('../')

from app import app  # NOQA
from user_service import Accessor  # NOQA


def test_ping():
    resp = app.test_client().get('/ping')
    assert resp.status_code == 200
    assert resp.data == b'{"ping": "pong"}\n'

def test_create_user():
    resp = app.test_client().post('/user/create/mike')
    assert resp.status_code == 201

def test_get_user():
    resp = app.test_client().get('/user/get/ae20d45c-5545-4389-9d1d-8c161be26160')
    assert resp.status_code == 404
    assert resp.data == b'{"user_fetched": false, "error": "User not found"}\n'
