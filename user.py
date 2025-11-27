from enum import Enum

class UserType(Enum):
    OWNER = 1
    USER = 2

class User:
    def __init__(self, name, uid, gid):
        self.name = name
        self.uid = uid
        self.gid = gid
        self.type = UserType.USER

    def __repr__(self):
        return f"User({self.name}, uid={self.uid}, gid={self.gid})"