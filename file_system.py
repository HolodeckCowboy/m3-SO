from file_type import FileType
from file import File


class Node:
    def __init__(self, name, is_dir=False, parent=None, file_obj=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = {} if is_dir else None
        self.file = file_obj


class FileSystem:
    def __init__(self, disk_manager, permission_manager):
        self.root = Node("/", is_dir=True)
        self.current_dir = self.root
        self.disk = disk_manager
        self.pm = permission_manager

    def get_pwd(self):
        if self.current_dir == self.root:
            return "/"
        path = ""
        node = self.current_dir
        while node.parent is not None:
            path = "/" + node.name + path
            node = node.parent
        return path

    def mkdir(self, name, user):
        if name in self.current_dir.children:
            return "Erro: Diretório já existe."
        new_dir = Node(name, is_dir=True, parent=self.current_dir)
        self.current_dir.children[name] = new_dir
        return f"Diretório '{name}' criado."

    def touch(self, name, user):
        if name in self.current_dir.children:
            return "Erro: Arquivo já existe."
        new_file_fcb = File(name, user, disk_ref=self.disk)
        new_node = Node(name, is_dir=False, parent=self.current_dir, file_obj=new_file_fcb)
        self.current_dir.children[name] = new_node
        return f"Arquivo '{name}' criado."

    def cd(self, path):
        if path == "..":
            if self.current_dir.parent:
                self.current_dir = self.current_dir.parent
            return ""
        if path == "/":
            self.current_dir = self.root
            return ""
        if path in self.current_dir.children:
            node = self.current_dir.children[path]
            if node.is_dir:
                self.current_dir = node
                return ""
            else:
                return f"Erro: '{path}' não é um diretório."
        return f"Erro: '{path}' não encontrado."

    def ls(self):
        output = []
        output.append(f"Conteúdo de {self.get_pwd()}:")
        for name, node in self.current_dir.children.items():
            type_str = "<DIR>" if node.is_dir else "<FILE>"
            meta = ""
            if not node.is_dir:
                perm = oct(node.file.permissions)[2:]
                size = node.file.size
                meta = f"(Perm: {perm}, Size: {size}, Inode: {node.file.id})"
            output.append(f"  {type_str}\t{name}\t{meta}")
        return "\n".join(output)

    def rm(self, name, user):
        if name not in self.current_dir.children:
            return "Erro: Arquivo não encontrado."

        node = self.current_dir.children[name]

        if not node.is_dir:
            if not self.pm.check_permission(node.file, user, 'w'):
                return "Erro: Permissão negada."

            if node.file.blocks:
                self.disk.free(node.file.blocks)

        del self.current_dir.children[name]
        return f"'{name}' removido."

    def cp(self, src_name, dest_name, user):
        """Copia um arquivo."""
        if src_name not in self.current_dir.children:
            return "Erro: Origem não encontrada."
        if dest_name in self.current_dir.children:
            return "Erro: Destino já existe."

        src_node = self.current_dir.children[src_name]
        if src_node.is_dir:
            return "Erro: cp não implementado para diretórios (use recursivo manualmente)."

        if not self.pm.check_permission(src_node.file, user, 'r'):
            return "Erro: Permissão de leitura negada na origem."

        content = src_node.file.cat()

        self.touch(dest_name, user)
        dest_node = self.current_dir.children[dest_name]

        dest_node.file.echo(content)
        return f"'{src_name}' copiado para '{dest_name}'."

    def mv(self, src_name, dest_name, user):
        if src_name not in self.current_dir.children:
            return "Erro: Origem não encontrada."

        if dest_name in self.current_dir.children:
            return "Erro: Destino já existe."

        node = self.current_dir.children.pop(src_name)
        node.name = dest_name
        if not node.is_dir:
            node.file.name = dest_name
            node.file.touch()

        self.current_dir.children[dest_name] = node
        return f"'{src_name}' movido para '{dest_name}'."

    def write_file(self, name, content, user):
        if name in self.current_dir.children:
            node = self.current_dir.children[name]
            if not node.is_dir:
                if self.pm.check_permission(node.file, user, 'w'):
                    node.file.echo(content)
                    return "Conteúdo escrito."
                return "Permissão negada (Write)."
            return f"'{name}' é um diretório."
        return "Arquivo não encontrado."

    def read_file(self, name, user):
        if name in self.current_dir.children:
            node = self.current_dir.children[name]
            if not node.is_dir:
                if self.pm.check_permission(node.file, user, 'r'):
                    return node.file.cat()
                return "Permissão negada (Read)."
            return f"'{name}' é um diretório."
        return "Arquivo não encontrado."

    def chmod_file(self, name, mode, user):
        if name in self.current_dir.children:
            node = self.current_dir.children[name]
            if not node.is_dir:
                self.pm.chmod(node.file, user, mode)
                return f"Permissões de '{name}' alteradas."
        return "Arquivo não encontrado."