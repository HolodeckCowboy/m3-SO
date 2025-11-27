class MemoryDisk:
    def __init__(self, total_blocks=100, block_size=10):
        self.block_size = block_size
        self.blocks = [None] * total_blocks  # O "disco" físico
        self.total_blocks = total_blocks

    def allocate(self, content):
        chunks = [content[i:i + self.block_size] for i in range(0, len(content), self.block_size)]

        allocated_indices = []

        try:
            for chunk in chunks:
                free_index = self.blocks.index(None)
                self.blocks[free_index] = chunk
                allocated_indices.append(free_index)
            return allocated_indices
        except ValueError:
            self.free(allocated_indices)
            raise Exception("Erro: Espaço em disco insuficiente.")

    def read(self, block_indices):
        content = ""
        for idx in block_indices:
            if 0 <= idx < self.total_blocks and self.blocks[idx] is not None:
                content += self.blocks[idx]
        return content

    def free(self, block_indices):
        for idx in block_indices:
            if 0 <= idx < self.total_blocks:
                self.blocks[idx] = None