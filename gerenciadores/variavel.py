from estruturas.bloco_variavel import BlocoVariavel

class GerenciadorVariavel:
    def __init__(self, tamanho_total, politica):
        self.tamanho_total = tamanho_total
        self.politica = politica 
        self.cabeca = BlocoVariavel(0, tamanho_total)
        self.ultimo_alocado = self.cabeca
        self.tabela_alocacao = {}

    def alocar(self, processo_id, tamanho_requisitado):
        bloco_escolhido = None

        if self.politica == 'worst-fit':
            maior_tamanho = -1
            atual = self.cabeca
            while atual:
                if atual.livre and atual.tamanho >= tamanho_requisitado:
                    if atual.tamanho > maior_tamanho:
                        maior_tamanho = atual.tamanho
                        bloco_escolhido = atual
                atual = atual.proximo

        elif self.politica == 'circular-fit':
            atual = self.ultimo_alocado
            primeira_passagem = True
            while atual:
                if atual.livre and atual.tamanho >= tamanho_requisitado:
                    bloco_escolhido = atual
                    break
                atual = atual.proximo
                if atual is None:
                    atual = self.cabeca
                if atual == self.ultimo_alocado and not primeira_passagem:
                    break 
                primeira_passagem = False

        if not bloco_escolhido:
            print("ESPAÇO INSUFICIENTE DE MEMÓRIA")
            return False

        if bloco_escolhido.tamanho > tamanho_requisitado:
            novo_bloco = BlocoVariavel(
                bloco_escolhido.inicio + tamanho_requisitado,
                bloco_escolhido.tamanho - tamanho_requisitado
            )
            novo_bloco.anterior = bloco_escolhido
            novo_bloco.proximo = bloco_escolhido.proximo
            if bloco_escolhido.proximo:
                bloco_escolhido.proximo.anterior = novo_bloco
            bloco_escolhido.proximo = novo_bloco
            bloco_escolhido.tamanho = tamanho_requisitado

        bloco_escolhido.livre = False
        bloco_escolhido.processo_id = processo_id
        self.tabela_alocacao[processo_id] = bloco_escolhido
        self.ultimo_alocado = bloco_escolhido
        return True

    def liberar(self, processo_id):
        if processo_id not in self.tabela_alocacao: 
            return False
            
        bloco = self.tabela_alocacao.pop(processo_id)
        bloco.livre = True
        bloco.processo_id = None

        if bloco.proximo and bloco.proximo.livre:
            bloco.tamanho += bloco.proximo.tamanho
            bloco.proximo = bloco.proximo.proximo
            if bloco.proximo:
                bloco.proximo.anterior = bloco
            if self.ultimo_alocado == bloco.proximo:
                self.ultimo_alocado = bloco

        if bloco.anterior and bloco.anterior.livre:
            anterior = bloco.anterior
            anterior.tamanho += bloco.tamanho
            anterior.proximo = bloco.proximo
            if bloco.proximo:
                bloco.proximo.anterior = anterior
            if self.ultimo_alocado == bloco:
                self.ultimo_alocado = anterior

        return True

    def listar_blocos_livres(self):
        blocos_livres = []
        atual = self.cabeca
        while atual:
            if atual.livre:
                blocos_livres.append(str(atual.tamanho))
            atual = atual.proximo
        saida = " | ".join(blocos_livres)
        return f"| {saida} |" if saida else "|"