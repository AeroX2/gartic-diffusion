import json
from uuid import uuid4


class User(json.JSONEncoder):
    def __init__(self, sid: str, name: str):
        self.sid = sid
        self.name = name

    def __hash__(self):
        return hash(self.sid)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.sid == other.sid
        return False

    def serialize(self):
        return {"sid": self.sid, "name": self.name}


class Lobby(json.JSONEncoder):
    def __init__(self):
        self.uuid = str(uuid4())
        self.users = set()

        self.game_state = "initial"
        self.rounds = 20
        self.current_round = 0

    def add_user(self, user: User):
        self.users.add(user)

    def remove_user(self, user: User):
        self.users.remove(user)

    def has_user(self, user: User) -> bool:
        return user in self.users

    def empty(self):
        return len(self.users) <= 0

    def serialize(self):
        return {
            "uuid": self.uuid,
            "users": list(map(lambda user: user.serialize(), self.users)),
        }
