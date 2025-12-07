from file_type import FileType
from file import File

class Node:
    """
    Representa um nó na árvore do sistema de arquivos.
    Pode ser um diretório (contendo filhos) ou um arquivo (contendo um objeto File).
    """
    def __init__(self, name, is_dir=False, parent=None, file_obj=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        # Se for diretório, inicializa dicionário de filhos; caso contrário, None.
        self.children = {} if is_dir else None
        # Referência ao objeto File (FCB) se for um arquivo.
        self.file = file_obj


class FileSystem:
    """
    Controlador principal do sistema de arquivos.
    Gerencia a navegação, criação e exclusão de nós e interage com o disco e permissões.
    """
    def __init__(self, disk_manager, permission_manager):
        # Inicializa a raiz do sistema
        self.root = Node("/", is_dir=True)
        self.current_dir = self.root
        self.disk = disk_manager
        self.pm = permission_manager

    def get_pwd(self):
        """Retorna o caminho absoluto do diretório atual."""
        if self.current_dir == self.root:
            return "/"
        path = ""
        node = self.current_dir
        # Percorre a árvore de baixo para cima até a raiz
        while node.parent is not None:
            path = "/" + node.name + path
            node = node.parent
        return path

    def mkdir(self, name, user):
        """Cria um novo diretório no diretório atual."""
        if name in self.current_dir.children:
            return "Erro: Diretório já existe."
        new_dir = Node(name, is_dir=True, parent=self.current_dir)
        self.current_dir.children[name] = new_dir
        return f"Diretório '{name}' criado."

    def touch(self, name, user):
        """Cria um arquivo vazio e o associa a um novo nó."""
        if name in self.current_dir.children:
            return "Erro: Arquivo já existe."
        # Cria o FCB (File Control Block)
        new_file_fcb = File(name, user, disk_ref=self.disk)
        # Cria o nó na árvore e associa o FCB
        new_node = Node(name, is_dir=False, parent=self.current_dir, file_obj=new_file_fcb)
        self.current_dir.children[name] = new_node
        return f"Arquivo '{name}' criado."

    def cd(self, path):
        """Navega entre diretórios (suporta '..' e '/')."""
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
        """Lista o conteúdo do diretório atual com metadados básicos."""
        output = []
        output.append(f"Conteúdo de {self.get_pwd()}:")
        for name, node in self.current_dir.children.items():
            type_str = "<DIR>" if node.is_dir else "<FILE>"
            meta = ""
            if not node.is_dir:
                # Converte permissões para octal e exibe tamanho/inode
                perm = oct(node.file.permissions)[2:]
                size = node.file.size
                meta = f"(Perm: {perm}, Size: {size}, Inode: {node.file.id})"
            output.append(f"  {type_str}\t{name}\t{meta}")
        return "\n".join(output)

    def rm(self, name, user):
        """Remove arquivos ou diretórios e libera blocos de memória."""
        if name not in self.current_dir.children:
            return "Erro: Arquivo não encontrado."

        node = self.current_dir.children[name]

        if not node.is_dir:
            # Verifica permissão de escrita no arquivo para poder removê-lo
            if not self.pm.check_permission(node.file, user, 'w'):
                return "Erro: Permissão negada."

            # Libera os blocos no disco virtual
            if node.file.blocks:
                self.disk.free(node.file.blocks)

        del self.current_dir.children[name]
        return f"'{name}' removido."

    def cp(self, src_name, dest_name, user):
        """
        Copia um arquivo.
        Lê o conteúdo da origem e escreve em um novo arquivo de destino.
        """
        if src_name not in self.current_dir.children:
            return "Erro: Origem não encontrada."
        if dest_name in self.current_dir.children:
            return "Erro: Destino já existe."

        src_node = self.current_dir.children[src_name]
        if src_node.is_dir:
            return "Erro: cp não implementado para diretórios (use recursivo manualmente)."

        # Verifica permissão de leitura na origem
        if not self.pm.check_permission(src_node.file, user, 'r'):
            return "Erro: Permissão de leitura negada na origem."

        # Lê conteúdo da memória
        content = src_node.file.cat()

        # Cria arquivo de destino e escreve o conteúdo
        self.touch(dest_name, user)
        dest_node = self.current_dir.children[dest_name]

        dest_node.file.echo(content)
        return f"'{src_name}' copiado para '{dest_name}'."

    def mv(self, src_name, dest_name, user):
        """Renomeia ou move um arquivo (nesta impl, apenas renomeia no dir atual)."""
        if src_name not in self.current_dir.children:
            return "Erro: Origem não encontrada."

        if dest_name in self.current_dir.children:
            return "Erro: Destino já existe."

        node = self.current_dir.children.pop(src_name)
        node.name = dest_name
        if not node.is_dir:
            node.file.name = dest_name
            node.file.touch() # Atualiza timestamp

        self.current_dir.children[dest_name] = node
        return f"'{src_name}' movido para '{dest_name}'."

    def write_file(self, name, content, user):
        """Escreve texto em um arquivo existente, verificando permissões."""
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
        """Lê o conteúdo de um arquivo, verificando permissões."""
        if name in self.current_dir.children:
            node = self.current_dir.children[name]
            if not node.is_dir:
                if self.pm.check_permission(node.file, user, 'r'):
                    return node.file.cat()
                return "Permissão negada (Read)."
            return f"'{name}' é um diretório."
        return "Arquivo não encontrado."

    def chmod_file(self, name, mode, user):
        """Altera as permissões (modo octal) de um arquivo."""
        if name in self.current_dir.children:
            node = self.current_dir.children[name]
            if not node.is_dir:
                self.pm.chmod(node.file, user, mode)
                return f"Permissões de '{name}' alteradas."
        return "Arquivo não encontrado."