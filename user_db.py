from db_driver import DBDriver
import psycopg2
import uuid
from psycopg2 import Error, extras

ERROR_USER_NOT_FOUND = "User not found"


class UserDB:
    def __init__(self, db_config):
        self.db_driver = DBDriver()
        self.db_driver.connect(db_config)
        self.db_driver.create_users_table()

    def create_user(self, user_details):
        psycopg2.extras.register_uuid()
        create_user_query = '''INSERT INTO users(id, name, created_at, updated_at) VALUES ((%s), (%s), now(), now())'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(create_user_query, [user_details["id"],
                                               user_details["name"]])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
            return {"user_created": False,
                    "error": err}
        else:
            return {"user_created": True}
        finally:
            cursor.close()

    def get_user(self, user_id):
        psycopg2.extras.register_uuid()
        get_user_query = '''SELECT id, name, created_at, updated_at FROM users WHERE id = (%s)'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(get_user_query, [user_id])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
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
        finally:
            cursor.close()


