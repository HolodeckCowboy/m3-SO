class MemoryDisk:
    """
    Simula um disco físico dividido em blocos.
    Gerencia a alocação e liberação de espaço (blocos).
    """
    def __init__(self, total_blocks=100, block_size=10):
        self.block_size = block_size
        # O "disco" físico: vetor onde cada posição é um bloco
        self.blocks = [None] * total_blocks
        self.total_blocks = total_blocks

    def allocate(self, content):
        """
        Tenta alocar conteúdo no disco.
        Divide o conteúdo em chunks e procura blocos livres sequencialmente ou dispersos.
        """
        # Divide o conteúdo em pedaços do tamanho do bloco
        chunks = [content[i:i + self.block_size] for i in range(0, len(content), self.block_size)]

        allocated_indices = []

        try:
            for chunk in chunks:
                # Encontra o próximo índice livre (lança ValueError se cheio)
                free_index = self.blocks.index(None)
                self.blocks[free_index] = chunk
                allocated_indices.append(free_index)
            return allocated_indices # Retorna lista de blocos usados (FAT simulada)
        except ValueError:
            # Rollback: se faltar espaço no meio, libera o que já foi alocado
            self.free(allocated_indices)
            raise Exception("Erro: Espaço em disco insuficiente.")

    def read(self, block_indices):
        """Reconstrói o conteúdo lendo a lista de blocos fornecida."""
        content = ""
        for idx in block_indices:
            if 0 <= idx < self.total_blocks and self.blocks[idx] is not None:
                content += self.blocks[idx]
        return content

    def free(self, block_indices):
        """Libera os blocos marcando-os como None."""
        for idx in block_indices:
            if 0 <= idx < self.total_blocks:
                self.blocks[idx] = None