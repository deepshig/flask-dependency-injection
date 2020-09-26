import uuid
import sys
import psycopg2
from psycopg2 import Error
sys.path.append('../')

from user_db import UserDB, ERROR_USER_NOT_FOUND  # NOQA
from user_service import Accessor  # NOQA

test_db_config = {"user": "postgres",
                  "password": "postgres",
                  "host": "127.0.0.1",
                  "port": "5432",
                  "db_name": "user_test"}


def tear_down(cursor, db_driver):
    cursor.execute("TRUNCATE users;")
    db_driver.connection.commit()
    cursor.close()
    db_driver.connection.close()


def test_create_user():
    """
    success
    """
    db = UserDB(test_db_config)
    accessor = Accessor(db)

    result = accessor.create_user("user1")
    assert result["user_created"] == True
    assert result["name"] == "user1"

    cursor = accessor.db.db_driver.connection.cursor()
    fetched_user = get_test_user(accessor.db, cursor, result["id"])
    assert fetched_user["user_fetched"] == True
    assert fetched_user["name"] == "user1"

    tear_down(cursor, accessor.db.db_driver)


def test_get_user():
    """
    failure : user does not exist
    """
    db = UserDB(test_db_config)
    accessor = Accessor(db)

    user_id = uuid.uuid4()
    access_token = uuid.uuid4()

    fetched_user = accessor.get_user(user_id)
    assert fetched_user["user_fetched"] == False
    assert fetched_user["error"] == ERROR_USER_NOT_FOUND

    """
    success
    """
    cursor = accessor.db.db_driver.connection.cursor()
    create_test_user(accessor.db, cursor, user_id)
    fetched_user = accessor.get_user(user_id)
    assert fetched_user["user_fetched"] == True
    assert fetched_user["id"] == user_id
    assert fetched_user["name"] == "user1"

    tear_down(cursor, accessor.db.db_driver)


def create_test_user(db, cursor, user_id):
    create_user_query = '''INSERT INTO users(id, name, created_at, updated_at) VALUES ((%s), (%s), now(), now())'''
    psycopg2.extras.register_uuid()

    try:
        cursor.execute(create_user_query, [
            user_id, "user1"])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error in creating test user : ", err)


def get_test_user(db, cursor, user_id):
    get_user_query = '''SELECT id, name, created_at, updated_at FROM users WHERE id = (%s)'''
    try:
        cursor.execute(get_user_query, [user_id])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error while fetching the test user : ", err)
        return {"user_fetched": False,
                "error": err}
    else:
        user = cursor.fetchone()
        if user is not None:
            return {"user_fetched": True,
                    "id": user[0],
                    "name": user[1],
                    "created_at": user[2],
                    "updated_at": user[3]}
        else:
            return {"user_fetched": False,
                    "error": ERROR_USER_NOT_FOUND}
