import re
import os
from gerenciadores.buddy import GerenciadorBuddy
from gerenciadores.variavel import GerenciadorVariavel

def processar_arquivo(caminho_arquivo, gerenciador):
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return

    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    print("Estado Inicial:", gerenciador.listar_blocos_livres())

    for linha in linhas:
        linha = linha.strip()
        if not linha: continue

        match_in = re.match(r'IN\(([A-Za-z0-9_]+),\s*(\d+)\)', linha)
        match_out = re.match(r'OUT\(([A-Za-z0-9_]+)\)', linha)

        if match_in:
            processo = match_in.group(1)
            tamanho = int(match_in.group(2))
            gerenciador.alocar(processo, tamanho)
        elif match_out:
            processo = match_out.group(1)
            gerenciador.liberar(processo)
        
        estado = gerenciador.listar_blocos_livres()
        
        if isinstance(gerenciador, GerenciadorBuddy):
            print(f"{linha.ljust(15)} {estado} (Fragmentação Interna: {gerenciador.fragmentacao_interna_total} KB)")
        else:
            print(f"{linha.ljust(15)} {estado}")

def main():
    print("--- Trabalho Prático 2: Gerenciamento de Memória ---")
    print("1. Partições Variáveis (Worst-Fit)")
    print("2. Partições Variáveis (Circular-Fit)")
    print("3. Sistema Buddy")
    
    escolha = input("Escolha a estratégia (1/2/3): ")
    tamanho = int(input("Informe o tamanho inicial da memória: "))
    
    arquivo_padrao = "entradas/requisicoes.txt"
    arquivo = input(f"Informe o caminho do arquivo de requisições [Padrão: {arquivo_padrao}]: ")
    
    if not arquivo.strip():
        arquivo = arquivo_padrao

    if escolha == '1':
        gerenciador = GerenciadorVariavel(tamanho, 'worst-fit')
    elif escolha == '2':
        gerenciador = GerenciadorVariavel(tamanho, 'circular-fit')
    elif escolha == '3':
        gerenciador = GerenciadorBuddy(tamanho)
    else:
        print("Opção inválida.")
        return

    print("\nProcessando requisições...")
    processar_arquivo(arquivo, gerenciador)

if __name__ == "__main__":
    main()