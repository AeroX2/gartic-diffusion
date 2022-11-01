import json
from uuid import uuid4


class User(json.JSONEncoder):
    def __init__(self, name):
        self.uuid = uuid4()
        self.name = name

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.uuid == other.uuid
        return False

    def serialize(self):
        return {"uuid": str(self.uuid), "name": self.name}


class Lobby(json.JSONEncoder):
    def __init__(self):
        self.uuid = str(uuid4())
        self.users = set()

    def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        self.users.remove(user)

    def serialize(self):
        return {
            "uuid": self.uuid,
            "users": list(map(lambda user: user.serialize(), self.users)),
        }
