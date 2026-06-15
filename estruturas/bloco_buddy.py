class BlocoMemoria:
    def __init__(self, tamanho, inicio):
        self.tamanho = tamanho
        self.inicio = inicio
        self.livre = True
        self.processo_id = None
        self.tamanho_requisitado = 0
        self.esquerda = None
        self.direita = None

    def eh_folha(self):
        return self.esquerda is None and self.direita is None