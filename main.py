import sys
from user import User
from memory_disk import MemoryDisk
from permission_manager import PermissionManager
from file_system import FileSystem


def print_help():
    """
    Exibe o manual de ajuda com os comandos suportados pelo shell.
    """
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
    # --- 1. Inicialização do Sistema (Boot) ---
    # Instancia o Hardware simulado (Disco de Memória)
    # Define um disco pequeno de 100 blocos, onde cada bloco armazena 10 caracteres.
    disk = MemoryDisk(total_blocks=100, block_size=10)

    # Instancia o gerenciador de segurança (Permissões)
    perm_mgr = PermissionManager()

    # Instancia o Sistema de Arquivos (Kernel/FS Layer), injetando as dependências de disco e permissões.
    fs = FileSystem(disk, perm_mgr)

    # --- 2. Configuração de Usuário Inicial ---
    # Cria o usuário 'root' (Superusuário) para iniciar a sessão.
    current_user = User("root", uid=0, gid=0)

    # Simula um banco de dados de usuários em memória (ex: /etc/passwd simplificado)
    users_db = {"root": current_user}

    print("=== Simulador de SO: M3-SO ===")
    print("Digite 'help' para ver os comandos.\n")

    # --- 3. Loop Principal (Shell / REPL) ---
    while True:
        try:
            # Obtém o caminho atual para exibir no prompt (ex: root@/docs $ )
            path = fs.get_pwd()
            command_input = input(f"{current_user.name}@{path} $ ").strip()

            # Ignora entradas vazias (apenas Enter)
            if not command_input:
                continue

            # Parser: Divide o comando e os argumentos
            parts = command_input.split()
            cmd = parts[0]
            args = parts[1:]

            # --- 4. Processamento de Comandos ---

            if cmd == "exit":
                print("Encerrando simulação...")
                break

            elif cmd == "help":
                print_help()

            elif cmd == "ls":
                # Lista conteúdo do diretório atual
                print(fs.ls())

            elif cmd == "pwd":
                # Print Working Directory
                print(fs.get_pwd())

            elif cmd == "mkdir":
                # Cria diretório se houver argumento
                if args:
                    print(fs.mkdir(args[0], current_user))
                else:
                    print("Uso: mkdir <nome>")

            elif cmd == "cd":
                # Navegação de diretórios
                if args:
                    msg = fs.cd(args[0])
                    if msg: print(msg)
                else:
                    print("Uso: cd <path>")

            elif cmd == "touch":
                # Cria arquivo vazio (atualiza timestamp se existir)
                if args:
                    print(fs.touch(args[0], current_user))
                else:
                    print("Uso: touch <nome>")

            elif cmd == "rm":
                # Remove arquivo ou diretório
                if args:
                    print(fs.rm(args[0], current_user))
                else:
                    print("Uso: rm <nome>")

            elif cmd == "cp":
                # Cópia de arquivos (Source -> Destination)
                if len(args) >= 2:
                    print(fs.cp(args[0], args[1], current_user))
                else:
                    print("Uso: cp <origem> <destino>")

            elif cmd == "mv":
                # Mover ou Renomear arquivos
                if len(args) >= 2:
                    print(fs.mv(args[0], args[1], current_user))
                else:
                    print("Uso: mv <origem> <destino>")

            elif cmd == "cat":
                # Leitura de arquivo (concatena blocos e exibe)
                if args:
                    print(fs.read_file(args[0], current_user))
                else:
                    print("Uso: cat <nome>")

            elif cmd == "write":
                # Escrita em arquivo (Simula editor de texto simples via CLI)
                # Junta todos os argumentos após o nome do arquivo como conteúdo
                if len(args) >= 2:
                    filename = args[0]
                    content = " ".join(args[1:])
                    print(fs.write_file(filename, content, current_user))
                else:
                    print("Uso: write <nome> <texto>")

            elif cmd == "chmod":
                # Altera permissões (exige formato octal)
                if len(args) >= 2:
                    try:
                        mode = int(args[0], 8)  # Converte string base 8 para int
                        print(fs.chmod_file(args[1], mode, current_user))
                    except ValueError:
                        print("Erro: Modo deve ser um número octal (ex: 755).")
                else:
                    print("Uso: chmod <modo_octal> <nome>")

            elif cmd == "disk":
                # Ferramenta de diagnóstico: Mostra estado físico do disco
                print(f"Blocos Livres: {disk.blocks.count(None)}/{disk.total_blocks}")
                # Visualização simplificada dos primeiros 50 blocos
                print(f"Mapa Visual: {['#' if b else '.' for b in disk.blocks[:50]]} ...")

            elif cmd == "su":
                # Switch User (Simulado)
                # Se o usuário não existe, o simulador cria automaticamente para facilitar testes
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
            # Captura genérica de erros para não derrubar o shell
            print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()