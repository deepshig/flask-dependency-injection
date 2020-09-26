import pytest
import uuid
import sys
import psycopg2
from psycopg2 import Error
sys.path.append('../')

from user_db import UserDB, ERROR_USER_NOT_FOUND  # NOQA


def test_db():
    test_db_config = {"user": "postgres",
                      "password": "postgres",
                      "host": "127.0.0.1",
                      "port": "5432",
                      "db_name": "user_test"}

    db = UserDB(test_db_config)
    return db


def tear_down(cursor, db_driver):
    cursor.execute("TRUNCATE users;")
    db_driver.connection.commit()
    cursor.close()
    db_driver.connection.close()


def test_create_user():
    """
    success
    """
    db = test_db()
    user_details = {"id": uuid.uuid4(),
                    "name": "dummy"}
    result = db.create_user(user_details)
    assert result["user_created"] == True

    fetch_user_query = '''SELECT * FROM users WHERE id = %s'''
    try:
        cursor = db.db_driver.connection.cursor()
        cursor.execute(fetch_user_query, [user_details["id"]])
        db.db_driver.connection.commit()

        fetched_user = cursor.fetchone()

        assert fetched_user[1] == user_details["name"]
    except psycopg2.Error as err:
        print("Error while checking if user created : ", err)

    """
    failure : when user_id is not uuid
    """
    user_details = {"id": "some_random_id",
                    "name": "dummy"}
    result = db.create_user(user_details)
    assert result["user_created"] == False
    assert result["error"].pgcode == '22P02'

    # tear_down(cursor, db.db_driver)


def test_get_user():
    db = test_db()
    """
    failure : user does not exist
    """
    new_user_id = uuid.uuid4()
    fetched_user = db.get_user(new_user_id)
    print(new_user_id)
    print(fetched_user)
    assert fetched_user["user_fetched"] == False
    assert fetched_user["error"] == ERROR_USER_NOT_FOUND

    """
    success
    """
    user_id = uuid.uuid4()

    create_user_query = '''INSERT INTO users(id, name, created_at, updated_at) VALUES ((%s), (%s), now(), now())'''
    cursor = db.db_driver.connection.cursor()
    psycopg2.extras.register_uuid()

    try:
        cursor.execute(create_user_query, [user_id, "dummy"])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error in creating test user : ", err)

    fetched_user = db.get_user(user_id)
    assert fetched_user["user_fetched"] == True

    tear_down(cursor, db.db_driver)
