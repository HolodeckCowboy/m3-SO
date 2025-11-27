import sys
from user import User
from memory_disk import MemoryDisk
from permission_manager import PermissionManager
from file_system import FileSystem


def print_help():
    print("""
    Comandos Disponíveis:
    ---------------------
    Navegação:
      ls                  - Listar diretório atual
      cd <dir>            - Mudar diretório (.. para voltar)
      pwd                 - Mostrar caminho atual
      mkdir <nome>        - Criar diretório

    Arquivos:
      touch <nome>        - Criar arquivo vazio
      rm <nome>           - Remover arquivo/diretório
      cp <src> <dst>      - Copiar arquivo
      mv <src> <dst>      - Mover/Renomear arquivo
      cat <nome>          - Ler conteúdo do arquivo
      write <nome> <txt>  - Escrever texto no arquivo (ex: write nota.txt ola)
      chmod <oct> <nome>  - Mudar permissões (ex: chmod 755 script.py)

    Sistema:
      su <user>           - Trocar usuário (simulação: cria se não existir)
      disk                - Mostrar mapa de blocos do disco
      help                - Mostrar esta ajuda
      exit                - Sair
    """)


def main():
    disk = MemoryDisk(total_blocks=100, block_size=10)
    perm_mgr = PermissionManager()
    fs = FileSystem(disk, perm_mgr)

    current_user = User("root", uid=0, gid=0)
    users_db = {"root": current_user}

    print("=== Simulador de SO: M3-SO ===")
    print("Digite 'help' para ver os comandos.\n")

    while True:
        try:
            path = fs.get_pwd()
            command_input = input(f"{current_user.name}@{path} $ ").strip()

            if not command_input:
                continue

            parts = command_input.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "exit":
                print("Encerrando simulação...")
                break

            elif cmd == "help":
                print_help()

            elif cmd == "ls":
                print(fs.ls())

            elif cmd == "pwd":
                print(fs.get_pwd())

            elif cmd == "mkdir":
                if args:
                    print(fs.mkdir(args[0], current_user))
                else:
                    print("Uso: mkdir <nome>")

            elif cmd == "cd":
                if args:
                    msg = fs.cd(args[0])
                    if msg: print(msg)
                else:
                    print("Uso: cd <path>")

            elif cmd == "touch":
                if args:
                    print(fs.touch(args[0], current_user))
                else:
                    print("Uso: touch <nome>")

            elif cmd == "rm":
                if args:
                    print(fs.rm(args[0], current_user))
                else:
                    print("Uso: rm <nome>")

            elif cmd == "cp":
                if len(args) >= 2:
                    print(fs.cp(args[0], args[1], current_user))
                else:
                    print("Uso: cp <origem> <destino>")

            elif cmd == "mv":
                if len(args) >= 2:
                    print(fs.mv(args[0], args[1], current_user))
                else:
                    print("Uso: mv <origem> <destino>")

            elif cmd == "cat":
                if args:
                    print(fs.read_file(args[0], current_user))
                else:
                    print("Uso: cat <nome>")

            elif cmd == "write":
                if len(args) >= 2:
                    filename = args[0]
                    content = " ".join(args[1:])
                    print(fs.write_file(filename, content, current_user))
                else:
                    print("Uso: write <nome> <texto>")

            elif cmd == "chmod":
                if len(args) >= 2:
                    try:
                        mode = int(args[0], 8)
                        print(fs.chmod_file(args[1], mode, current_user))
                    except ValueError:
                        print("Erro: Modo deve ser um número octal (ex: 755).")
                else:
                    print("Uso: chmod <modo_octal> <nome>")

            elif cmd == "disk":
                print(f"Blocos Livres: {disk.blocks.count(None)}/{disk.total_blocks}")
                print(f"Mapa Visual: {['#' if b else '.' for b in disk.blocks[:50]]} ...")

            elif cmd == "su":
                if args:
                    target_name = args[0]
                    if target_name in users_db:
                        current_user = users_db[target_name]
                    else:
                        new_uid = len(users_db) + 1000
                        new_user = User(target_name, uid=new_uid, gid=new_uid)
                        users_db[target_name] = new_user
                        current_user = new_user
                        print(f"Usuário criado e alterado para '{target_name}'")
                else:
                    print("Uso: su <usuario>")

            else:
                print(f"Comando '{cmd}' não reconhecido.")

        except Exception as e:
            print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()