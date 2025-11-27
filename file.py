import time
from file_type import FileType


class File:
    _id_counter = 1

    def __init__(self, name, user, file_type=FileType.CHAR, disk_ref=None):
        self.id = File._id_counter
        File._id_counter += 1

        self.name = name
        self.size = 0
        self.type = file_type

        now = time.time()
        self.created_at = now
        self.updated_at = now
        self.access_at = now

        self.uid = user.uid
        self.gid = user.gid
        self.permissions = 0o644

        self.disk = disk_ref
        self.blocks = []

    def touch(self):
        self.updated_at = time.time()

    def echo(self, content):
        if self.disk:
            if self.blocks:
                self.disk.free(self.blocks)

            try:
                self.blocks = self.disk.allocate(content)
                self.size = len(content)
                self.updated_at = time.time()
                print(f"Conteúdo escrito em {self.name}. Blocos alocados: {self.blocks}")
            except Exception as e:
                print(e)

    def cat(self):
        self.access_at = time.time()
        if self.disk and self.blocks:
            return self.disk.read(self.blocks)
        return ""

    def copy_meta_from(self, other_file):
        self.size = other_file.size
        self.type = other_file.type
        self.permissions = other_file.permissions