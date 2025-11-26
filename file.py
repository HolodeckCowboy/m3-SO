import copy

#TODO Implementar classe
class File:
    def __init__(self, args):
        self.name = ''
        self.size = ''
        self.type = ''
        self.created_at = ''
        self.updated_at = ''
        self.access_at = ''
        self.id = ''
        self.read_permission = False
        self.write_permission = False
        self.exec_permission = False
        self.current_content = ''
        self.current_user = ''
    
    def touch(self):
        pass

    def echo(self, content):
        self.current_content = content

    def cat (self):
        pass
    
    def copy(self, file):
        new_file = copy.deepcopy(file)
        return new_file
    
    def move(self):
        pass

    
    def remove(self):
        pass