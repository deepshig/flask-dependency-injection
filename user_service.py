import uuid
from injector import inject
from user_db import UserDB


class Accessor:
    def __init__(self, db):
        self.db = db

    def create_user(self, name):
        user_details = {"id": uuid.uuid4(),
                        "name": name}

        result = self.db.create_user(user_details)
        if result["user_created"]:
            user_details["user_created"] = True
            return user_details
        else:
            return result

    def get_user(self, user_id):
        fetched_user = self.db.get_user(user_id)
        if fetched_user["user_fetched"]:
                return fetched_user
        else:
            return fetched_user
