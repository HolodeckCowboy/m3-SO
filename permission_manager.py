class PermissionManager:
    READ = 4
    WRITE = 2
    EXECUTE = 1

    def __init__(self):
        pass

    def check_permission(self, file_obj, user, operation):
        perm_bits = file_obj.permissions

        if user.uid == file_obj.uid:
            shifted_perm = (perm_bits >> 6) & 0o7
        elif user.gid == file_obj.gid:
            shifted_perm = (perm_bits >> 3) & 0o7
        else:
            shifted_perm = perm_bits & 0o7

        required = 0
        if operation == 'r':
            required = self.READ
        elif operation == 'w':
            required = self.WRITE
        elif operation == 'x':
            required = self.EXECUTE

        return (shifted_perm & required) == required

    def chmod(self, file_obj, user, new_mode):
        if user.uid == file_obj.uid:
            file_obj.permissions = new_mode
            print(f"Permissões de '{file_obj.name}' alteradas para {oct(new_mode)}")
        else:
            print("Erro: Apenas o dono pode alterar permissões.")