import json
import threading
from typing import Optional
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


class Round:
    def __init__(self, round_number: int):
        self.round_number = round_number
        self.user_responses: dict[User, str] = {}


class Lobby(json.JSONEncoder):
    def __init__(self):
        self.uuid: str = str(uuid4())
        self.users: set[User] = set()

        self.game_state = "initial"
        self.lock = threading.Lock()

        self.rounds = [Round(0)]
        self.round_timer: int = 0
        self.amount_of_rounds: int = 0

    def add_user(self, user: User):
        self.users.add(user)

    def remove_user(self, user: User):
        self.users.remove(user)

    def has_user(self, user: User) -> bool:
        return user in self.users

    def empty(self):
        return len(self.users) <= 0

    def current_round(self) -> Round:
        self.lock.acquire()
        round = self.rounds[len(self.rounds)-1]
        self.lock.release()
        return round

    def new_round(self, round: int):
        self.lock.acquire()
        self.rounds.append(Round(round))
        self.lock.release()

    def current_responses(self):
        self.current_round().user_responses

    def add_response(self, user: User, description: str):
        self.current_round().user_responses[user] = description

    def all_responses_received(self) -> bool:
        return len(self.current_round().user_responses) == len(self.users)

    def serialize(self):
        return {
            "uuid": self.uuid,
            "users": list(map(lambda user: user.serialize(), self.users)),
        }
