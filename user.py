from enum import Enum

#TODO Definir funcionamento do grupo
class UserType(Enum):
    OWNER = 1
    USER = 2

class User:
    def __init__(self):
        self.type = ''
        self.group = ''


    def check_permission(self):
        pass