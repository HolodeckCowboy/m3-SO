class PermissionManager:
    """
    Gerencia verificações de permissão baseadas em bits (Unix-like).
    Bits: Read(4), Write(2), Execute(1).
    """
    READ = 4
    WRITE = 2
    EXECUTE = 1

    def __init__(self):
        pass

    def check_permission(self, file_obj, user, operation):
        """
        Verifica se o usuário tem permissão para a operação.
        Analisa Owner, Group ou Other dependendo do UID/GID.
        """
        perm_bits = file_obj.permissions

        if user.uid == file_obj.uid:
            # Desloca 6 bits para pegar a permissão de Dono (ex: 700 -> 7)
            shifted_perm = (perm_bits >> 6) & 0o7
        elif user.gid == file_obj.gid:
            # Desloca 3 bits para pegar a permissão de Grupo
            shifted_perm = (perm_bits >> 3) & 0o7
        else:
            # Pega os últimos 3 bits para Outros
            shifted_perm = perm_bits & 0o7

        required = 0
        if operation == 'r':
            required = self.READ
        elif operation == 'w':
            required = self.WRITE
        elif operation == 'x':
            required = self.EXECUTE

        # Verifica se o bit necessário está ativo usando AND bit a bit
        return (shifted_perm & required) == required

    def chmod(self, file_obj, user, new_mode):
        """Altera os bits de permissão de um arquivo."""
        if user.uid == file_obj.uid:
            file_obj.permissions = new_mode
            print(f"Permissões de '{file_obj.name}' alteradas para {oct(new_mode)}")
        else:
            print("Erro: Apenas o dono pode alterar permissões.")