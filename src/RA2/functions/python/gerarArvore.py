import os

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

class NoArvore:
    def __init__(self, label):
        self.label = label
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def desenhar_ascii(self, prefixo='', eh_ultimo=True):
        # Usa ASCII simples para compatibilidade Windows
        conector = '`-- ' if eh_ultimo else '|-- '
        resultado = prefixo + conector + self.label + '\n'
        prefixo_prox = prefixo + ('    ' if eh_ultimo else '|   ')
        for i, filho in enumerate(self.filhos):
            ultimo = i == len(self.filhos) - 1
            resultado += filho.desenhar_ascii(prefixo_prox, ultimo)
        return resultado

def gerarArvore(derivacao, simbolo_inicial='PROGRAM'):
    """
    Gera arvore sintatica a partir da derivacao produzida pelo parser.

    Args:
        derivacao: Lista de strings no formato "LHS -> RHS" ou "LHS → RHS"
                   Exemplo: ["PROGRAM -> LINHA PROGRAM_PRIME", "LINHA -> ( CONTENT )", ...]
        simbolo_inicial: Simbolo raiz da arvore (default: 'PROGRAM')

    Returns:
        NoArvore representando a raiz da arvore sintatica
    """
    # Processar derivacao - aceita tanto '->' quanto '→'
    producoes = []
    for linha in derivacao:
        # Tenta split com ambos separadores
        if '->' in linha:
            partes = linha.split('->')
        elif '→' in linha:
            partes = linha.split('→')
        else:
            continue  # Pula linhas sem separador

        if len(partes) == 2:
            lhs = partes[0].strip()
            rhs = partes[1].strip()

            # Trata EPSILON como producao vazia
            if rhs == 'EPSILON' or rhs == 'ε':
                rhs_simbolos = ['EPSILON']
            else:
                rhs_simbolos = rhs.split()

            producoes.append((lhs, rhs_simbolos))

    index = [0]  # indice mutavel

    def construir_no(simbolo_esperado):
        if index[0] >= len(producoes):
            return NoArvore(simbolo_esperado)

        lhs, rhs = producoes[index[0]]
        if lhs != simbolo_esperado:
            return NoArvore(simbolo_esperado)

        index[0] += 1
        no = NoArvore(lhs)
        for simbolo in rhs:
            if simbolo != 'EPSILON' and simbolo != 'ε':
                filho = construir_no(simbolo)
                no.adicionar_filho(filho)
            else:
                # Usa 'epsilon' ASCII para compatibilidade
                no.adicionar_filho(NoArvore('epsilon'))
        return no

    return construir_no(simbolo_inicial)

def exportar_arvore_ascii(arvore, nome_arquivo='arvore_output.txt'):
    conteudo = arvore.label + '\n'
    for i, filho in enumerate(arvore.filhos):
        eh_ultimo = i == len(arvore.filhos) - 1
        conteudo += filho.desenhar_ascii('', eh_ultimo)

    # Exportar para a raiz
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    # Exportar para /outputs/RA2/
    output_dir = os.path.join(os.getcwd(), 'outputs', 'RA2')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, nome_arquivo)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"Árvore exportada para: {nome_arquivo} e outputs/RA2/{nome_arquivo}")
