# m3-SO: Simulador de Sistema de Arquivos

## Visão Geral
O **m3-SO** é um simulador de sistema operacional desenvolvido em Python, focado na implementação e gestão de um sistema de arquivos. O projeto simula a interação entre a estrutura lógica de diretórios, o controle de permissões de usuários (Unix-like) e o gerenciamento físico de memória em blocos.

## Arquitetura do Sistema

O sistema é modular e composto pelos seguintes componentes principais:

* **FileSystem (`file_system.py`)**: Gerencia a árvore de diretórios (Nodes), navegação e operações de alto nível (CRUD de arquivos/pastas).
* **MemoryDisk (`memory_disk.py`)**: Simula um dispositivo de armazenamento baseado em blocos. Trata a fragmentação de dados dividindo o conteúdo em chunks de tamanho fixo.
* **File (`file.py`)**: Atua como o *File Control Block* (FCB), armazenando metadados (inode, timestamps, uid, gid, permissões) e a lista de ponteiros para os blocos no disco.
* **PermissionManager (`permission_manager.py`)**: Implementa a lógica de verificação de acesso baseada em bits (Read/Write/Execute) para Dono, Grupo e Outros.
* **User (`user.py`)**: Representação simplificada de usuários e grupos (UID/GID).
* **Main (`main.py`)**: Interface de Linha de Comando (CLI) que inicializa o kernel simulado e processa os comandos do usuário.

## Funcionalidades Implementadas

### Gerenciamento de Arquivos e Diretórios
* `ls`: Listagem de conteúdo com metadados.
* `mkdir`: Criação de diretórios.
* `touch`: Criação de arquivos vazios.
* `rm`: Remoção de arquivos e liberação de memória.
* `cp`: Cópia de arquivos (leitura e nova alocação).
* `mv`: Movimentação/Renomeação de arquivos.

### Gerenciamento de I/O e Memória
* `write`: Escrita de strings em arquivos (simula alocação de blocos).
* `cat`: Leitura de arquivos (reconstrução a partir dos blocos).
* `disk`: Visualização do mapa de blocos do disco (simulação de bitmap).

### Sistema de Permissões e Usuários
* `chmod`: Alteração de permissões em octal (ex: `755`).
* `su`: Troca de usuário (criação dinâmica para testes).
* Verificação rigorosa de permissões (`r`, `w`) antes de operações de leitura ou escrita.

## Como Executar

O projeto não possui dependências externas além do Python 3 padrão.

1.  Execute o arquivo principal:
    ```bash
    python main.py
    ```
2.  Utilize o comando `help` dentro da CLI para ver a lista de comandos disponíveis.

## Exemplo de Uso

```bash
root@/ $ mkdir docs
root@/ $ cd docs
root@/docs $ touch nota.txt
root@/docs $ write nota.txt OlaMundo
Conteúdo escrito em nota.txt. Blocos alocados: [0]
root@/docs $ ls
  <FILE>    nota.txt    (Perm: 644, Size: 8, Inode: 1)
root@/docs $ chmod 777 nota.txt
Permissões de 'nota.txt' alteradas para 0o777