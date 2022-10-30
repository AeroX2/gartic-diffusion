from uuid import uuid4

class User:
    def __init__(self, name):
        self.uuid = uuid4()
        self.name = name
        
    def __hash__(self):
        return self.uuid
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.uuid == other.uuid
        return False

class Lobby:
    def __init__(self):
        self.uuid = uuid4()
        self.users = set()
    
    def add_user(user):
        self.users.add(user)
        
    def remove_user(user):
        self.users.remove(user)