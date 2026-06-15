class BlocoVariavel:
    def __init__(self, inicio, tamanho, livre=True, processo_id=None):
        self.inicio = inicio
        self.tamanho = tamanho
        self.livre = livre
        self.processo_id = processo_id
        self.anterior = None
        self.proximo = None