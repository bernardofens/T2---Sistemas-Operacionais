import math
from estruturas.bloco_buddy import BlocoMemoria

class GerenciadorBuddy:
    def __init__(self, tamanho_total):
        self.tamanho_total = tamanho_total
        self.raiz = BlocoMemoria(tamanho_total, 0)
        self.tabela_alocacao = {}
        self.fragmentacao_interna_total = 0

    def _proxima_potencia_de_2(self, tamanho):
        if tamanho <= 0: return 0
        return 2 ** math.ceil(math.log2(tamanho))

    def alocar(self, processo_id, tamanho_requisitado):
        tamanho_necessario = self._proxima_potencia_de_2(tamanho_requisitado)
        if tamanho_necessario > self.tamanho_total:
            print("ESPAÇO INSUFICIENTE DE MEMÓRIA")
            return False
        
        bloco_alocado = self._buscar_e_dividir(self.raiz, tamanho_necessario, processo_id, tamanho_requisitado)
        if bloco_alocado:
            self.tabela_alocacao[processo_id] = bloco_alocado
            self.fragmentacao_interna_total += (tamanho_necessario - tamanho_requisitado)
            return True
        else:
            print("ESPAÇO INSUFICIENTE DE MEMÓRIA")
            return False

    def _buscar_e_dividir(self, no, tamanho_necessario, processo_id, tamanho_requisitado):
        if no.tamanho < tamanho_necessario:
            return None
            
        if no.eh_folha() and not no.livre:
            return None
            
        if no.eh_folha() and no.tamanho == tamanho_necessario:
            no.livre = False
            no.processo_id = processo_id
            no.tamanho_requisitado = tamanho_requisitado
            return no
            
        if no.eh_folha() and no.tamanho > tamanho_necessario:
            metade = no.tamanho // 2
            no.esquerda = BlocoMemoria(metade, no.inicio)
            no.direita = BlocoMemoria(metade, no.inicio + metade)
            no.livre = False 
            
        alocado_esq = self._buscar_e_dividir(no.esquerda, tamanho_necessario, processo_id, tamanho_requisitado)
        if alocado_esq:
            return alocado_esq
            
        alocado_dir = self._buscar_e_dividir(no.direita, tamanho_necessario, processo_id, tamanho_requisitado)
        if alocado_dir:
            return alocado_dir
            
        return None

    def liberar(self, processo_id):
        if processo_id not in self.tabela_alocacao: 
            return False
        
        bloco = self.tabela_alocacao.pop(processo_id)
        self.fragmentacao_interna_total -= (bloco.tamanho - bloco.tamanho_requisitado)
        
        bloco.livre = True
        bloco.processo_id = None
        bloco.tamanho_requisitado = 0
        
        self._coalescer(self.raiz)
        return True

    def _coalescer(self, no):
        if no is None or no.eh_folha(): 
            return
            
        self._coalescer(no.esquerda)
        self._coalescer(no.direita)
        
        if (no.esquerda.eh_folha() and no.esquerda.livre) and \
           (no.direita.eh_folha() and no.direita.livre):
            no.esquerda = None
            no.direita = None
            no.livre = True

    def listar_blocos_livres(self):
        blocos = []
        self._coletar_livres(self.raiz, blocos)
        blocos.sort(key=lambda b: b.inicio)
        saida = " | ".join([str(b.tamanho) for b in blocos])
        return f"| {saida} |" if saida else "|"

    def _coletar_livres(self, no, blocos):
        if no is None: 
            return
        if no.eh_folha():
            if no.livre: 
                blocos.append(no)
        else:
            self._coletar_livres(no.esquerda, blocos)
            self._coletar_livres(no.direita, blocos)