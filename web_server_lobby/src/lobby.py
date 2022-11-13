import json
import math
import random
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
    def __init__(self, round_number: int, shuffle_indicies: list[int]):
        self.round_number = round_number
        self.shuffle_indices = shuffle_indicies
        self.user_responses: dict[User, str] = {}


class Lobby(json.JSONEncoder):
    def __init__(self):
        self.uuid: str = str(uuid4())
        self.users: set[User] = set()

        self.game_state = "initial"
        self.lock = threading.Lock()

        self.rounds = []
        self.round_timer: int = 0
        self.amount_of_rounds: int = 0

        self.invalid_permutation = set()

    def add_user(self, user: User):
        self.users.add(user)

    def remove_user(self, user: User):
        self.users.remove(user)

    def has_user(self, user: User) -> bool:
        return user in self.users

    def empty(self) -> bool:
        return len(self.users) <= 0

    def new_game(self, round_timer: int):
        self.round_timer = round_timer

        user_len = len(self.users)
        self.amount_of_rounds = user_len

        self.new_round(first=True)

    def current_round(self) -> Round:
        self.lock.acquire()
        round = self.rounds[len(self.rounds)-1]
        self.lock.release()
        return round

    def _generate_shuffle(self) -> list[int]:
        n = len(self.users)
        i = random.randint(0, math.factorial(n))
        while i in self.invalid_permutation:
            i = random.randint(0, math.factorial(n))
        self.invalid_permutation.add(i)

        perm = [0] * n
        fact = [0] * n
        fact[0] = 1
        for k in range(n):
            fact[k] = fact[k - 1] * k

        for k in range(1,n):
            perm[k] = i // fact[n - 1 - k]
            i = i % fact[n - 1 - k]

        for k in range(n - 1, 0, -1):
            for j in range(k - 1, 0, -1):
                if (perm[j] <= perm[k]):
                    perm[k] += 1
        return perm

    def new_round(self, first = False) -> Round:
        self.lock.acquire()

        shuffle = [] if first else self._generate_shuffle()
        round = Round(len(self.rounds), shuffle)
        self.rounds.append(round)

        self.lock.release()
        return round

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
