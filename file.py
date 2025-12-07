import time
from file_type import FileType

class File:
    """
    File Control Block (FCB).
    Armazena metadados e ponteiros para os blocos de dados no disco.
    """
    _id_counter = 1

    def __init__(self, name, user, file_type=FileType.CHAR, disk_ref=None):
        self.id = File._id_counter
        File._id_counter += 1

        self.name = name
        self.size = 0
        self.type = file_type

        # Timestamps
        now = time.time()
        self.created_at = now
        self.updated_at = now
        self.access_at = now

        # Propriedade (Owner/Group) e Permissões padrão (rw-r--r--)
        self.uid = user.uid
        self.gid = user.gid
        self.permissions = 0o644

        self.disk = disk_ref
        self.blocks = [] # Lista de índices dos blocos no MemoryDisk

    def touch(self):
        """Atualiza data de modificação."""
        self.updated_at = time.time()

    def echo(self, content):
        """Escreve conteúdo no arquivo, alocando blocos no disco."""
        if self.disk:
            # Sobrescreve: Libera blocos antigos antes de alocar novos
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
        """Lê o conteúdo do disco baseado nos blocos alocados."""
        self.access_at = time.time()
        if self.disk and self.blocks:
            return self.disk.read(self.blocks)
        return ""

    def copy_meta_from(self, other_file):
        """Copia metadados de outro arquivo (usado em cp -p, se implementado)."""
        self.size = other_file.size
        self.type = other_file.type
        self.permissions = other_file.permissions