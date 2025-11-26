from enum import Enum
from user import User, UserType


class PermissionManager:

    def __init__(self, user):
        self.current_user = user

    def change_permission(self, file):
        if self.current_user.type == UserType.OWNER.value:
            file.read_permission = True
            file.write_permission = True
            file.exec_permission = True
        
        else:
            pass