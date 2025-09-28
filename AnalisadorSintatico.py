#!/usr/bin/env python3
"""
Função lerTokens para RA2 - Analisador Sintático LL(1)
Student 3 Responsibility

Esta função lê arquivo de tokens gerado na Fase 1 e adiciona novos tokens
para estruturas de controle (loops e decisões) e operadores relacionais.
"""

import sys
from pathlib import Path
from typing import List, Optional

# Definições de Token para RA2 (baseadas na RA1 + extensões)
# Usando definições locais para evitar problemas de import

class Tipo_de_Token:
    # Números
    NUMERO_REAL = "NUMERO_REAL"

    # Operadores aritméticos originais
    SOMA = "SOMA"
    SUBTRACAO = "SUBTRACAO"
    MULTIPLICACAO = "MULT"
    DIVISAO = "DIV"
    RESTO = "RESTO"
    POTENCIA = "POT"

    # Símbolos de agrupamento
    ABRE_PARENTESES = "ABRE_PARENTESES"
    FECHA_PARENTESES = "FECHA_PARENTESES"

    # Comandos especiais originais
    RES = "RES"
    MEM = "MEM"

    # NOVOS TOKENS para RA2 - Estruturas de controle
    RELATIONAL_OP = "RELATIONAL_OP"
    CONTROL_STRUCT = "CONTROL_STRUCT"
    LOGICAL_OP = "LOGICAL_OP"

    # Marcador de fim
    FIM = "FIM"

class Token:
    def __init__(self, tipo: str, valor, linha: int = 0, coluna: int = 0):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

def lerTokens(arquivo: str) -> List[Token]:
    """
    Lê arquivo de tokens gerado na Fase 1 e adiciona novos tokens para estruturas de controle.

    Args:
        arquivo: Nome do arquivo contendo tokens da Fase 1

    Returns:
        Lista de tokens processados incluindo novos tokens de controle

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o formato dos tokens for inválido

    Exemplo de uso:
        tokens = lerTokens("teste1.txt")
        for token in tokens:
            print(token)
    """
    tokens = []

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha_num, linha in enumerate(f, 1):
                linha = linha.strip()

                # Pular linhas vazias e comentários
                if not linha or linha.startswith('#'):
                    continue

                # Processar tokens da linha
                tokens_linha = processarLinha(linha, linha_num)
                tokens.extend(tokens_linha)

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de tokens não encontrado: {arquivo}")
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo de tokens: {e}")

    # Adicionar token de fim de arquivo
    tokens.append(Token(Tipo_de_Token.FIM, "$", len(tokens), 0))

    return tokens

def processarLinha(linha: str, linha_num: int) -> List[Token]:
    """
    Processa uma linha do arquivo de tokens, incluindo reconhecimento de novos tokens.

    Args:
        linha: Linha do arquivo
        linha_num: Número da linha para relatório de erros

    Returns:
        Lista de tokens da linha
    """
    tokens = []
    elementos = linha.split()

    for coluna, elemento in enumerate(elementos):
        token = reconhecerToken(elemento, linha_num, coluna)
        if token:
            tokens.append(token)

    return tokens

def reconhecerToken(elemento: str, linha: int, coluna: int) -> Optional[Token]:
    """
    Reconhece e classifica um token, incluindo novos tokens de estruturas de controle.

    Esta função implementa o reconhecimento de:
    1. Tokens originais da RA1 (operadores aritméticos, números, etc.)
    2. NOVOS tokens para RA2: operadores relacionais, estruturas de controle, operadores lógicos

    Args:
        elemento: String do elemento a ser tokenizado
        linha: Número da linha
        coluna: Posição na linha

    Returns:
        Token reconhecido ou None se inválido
    """

    # ===== NOVOS TOKENS PARA RA2 =====

    # Operadores relacionais (conforme especificação PDF)
    operadores_relacionais = {
        '>': 'MAIOR',
        '<': 'MENOR',
        '==': 'IGUAL',
        '>=': 'MAIOR_IGUAL',
        '<=': 'MENOR_IGUAL',
        '!=': 'DIFERENTE'
    }

    # Estruturas de controle (padrão RPN pós-fixado)
    estruturas_controle = {
        'IF': 'IF',           # Condicional simples: (condição ação IF)
        'IFELSE': 'IFELSE',   # Condicional com alternativa: (condição ação1 ação2 IFELSE)
        'WHILE': 'WHILE',     # Loop while: (condição ação WHILE)
        'FOR': 'FOR',         # Loop for: (início fim contador ação FOR)
        'ELSE': 'ELSE'        # Alternativa (para sintaxes específicas)
    }

    # Operadores lógicos
    operadores_logicos = {
        'AND': 'AND',
        'OR': 'OR',
        'NOT': 'NOT'
    }

    # ===== VERIFICAÇÃO DE NOVOS TOKENS =====

    # Verificar operadores relacionais
    if elemento in operadores_relacionais:
        return Token(Tipo_de_Token.RELATIONAL_OP, operadores_relacionais[elemento], linha, coluna)

    # Verificar estruturas de controle
    if elemento in estruturas_controle:
        return Token(Tipo_de_Token.CONTROL_STRUCT, estruturas_controle[elemento], linha, coluna)

    # Verificar operadores lógicos
    if elemento in operadores_logicos:
        return Token(Tipo_de_Token.LOGICAL_OP, operadores_logicos[elemento], linha, coluna)

    # ===== TOKENS ORIGINAIS DA RA1 =====

    # Símbolos de agrupamento
    if elemento == '(':
        return Token(Tipo_de_Token.ABRE_PARENTESES, elemento, linha, coluna)
    elif elemento == ')':
        return Token(Tipo_de_Token.FECHA_PARENTESES, elemento, linha, coluna)

    # Operadores aritméticos
    elif elemento == '+':
        return Token(Tipo_de_Token.SOMA, elemento, linha, coluna)
    elif elemento == '-':
        return Token(Tipo_de_Token.SUBTRACAO, elemento, linha, coluna)
    elif elemento == '*':
        return Token(Tipo_de_Token.MULTIPLICACAO, elemento, linha, coluna)
    elif elemento == '|':  # Divisão real
        return Token(Tipo_de_Token.DIVISAO, elemento, linha, coluna)
    elif elemento == '/':  # Divisão inteira
        return Token(Tipo_de_Token.DIVISAO, elemento, linha, coluna)
    elif elemento == '%':  # Resto (módulo)
        return Token(Tipo_de_Token.RESTO, elemento, linha, coluna)
    elif elemento == '^':  # Potência
        return Token(Tipo_de_Token.POTENCIA, elemento, linha, coluna)

    # Comandos especiais
    elif elemento == 'RES':
        return Token(Tipo_de_Token.RES, elemento, linha, coluna)
    elif elemento.upper() == 'MEM' or (elemento.isupper() and elemento.isalpha()):
        # Aceita MEM ou qualquer sequência de letras maiúsculas como memória
        # Conforme especificação: MEM pode ser qualquer conjunto de letras maiúsculas
        return Token(Tipo_de_Token.MEM, elemento, linha, coluna)

    # Números (inteiros e reais)
    else:
        try:
            # Verificar se é número inteiro
            int(elemento)
            return Token(Tipo_de_Token.NUMERO_REAL, elemento, linha, coluna)
        except ValueError:
            try:
                # Verificar se é número real (ponto flutuante)
                float(elemento)
                return Token(Tipo_de_Token.NUMERO_REAL, elemento, linha, coluna)
            except ValueError:
                # Token não reconhecido
                print(f"Aviso: Token não reconhecido '{elemento}' na linha {linha}, coluna {coluna}")
                return None

def validarTokens(tokens: List[Token]) -> bool:
    """
    Valida lista de tokens para verificar se estão em formato válido.

    Args:
        tokens: Lista de tokens para validar

    Returns:
        True se tokens são válidos, False caso contrário
    """
    if not tokens:
        print("Erro: Lista de tokens vazia")
        return False

    # Verificar se há parênteses balanceados
    contador_parenteses = 0
    for token in tokens:
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            contador_parenteses += 1
        elif token.tipo == Tipo_de_Token.FECHA_PARENTESES:
            contador_parenteses -= 1
            if contador_parenteses < 0:
                print(f"Erro: Parênteses desbalanceados na linha {token.linha}")
                return False

    if contador_parenteses != 0:
        print("Erro: Parênteses não balanceados no arquivo")
        return False

    # Verificar se último token é FIM
    if tokens[-1].tipo != Tipo_de_Token.FIM:
        print("Aviso: Token FIM não encontrado no final")

    return True

def exibirEstatisticasTokens(tokens: List[Token]) -> None:
    """
    Exibe estatísticas sobre os tokens processados.

    Args:
        tokens: Lista de tokens para analisar
    """
    contadores = {}
    novos_tokens = 0

    for token in tokens:
        contadores[token.tipo] = contadores.get(token.tipo, 0) + 1

        # Contar novos tokens da RA2
        if token.tipo in [Tipo_de_Token.RELATIONAL_OP, Tipo_de_Token.CONTROL_STRUCT, Tipo_de_Token.LOGICAL_OP]:
            novos_tokens += 1

    print(f"\n=== ESTATÍSTICAS DOS TOKENS ===")
    print(f"Total de tokens: {len(tokens)}")
    print(f"Novos tokens (RA2): {novos_tokens}")
    print(f"\nDistribuição por tipo:")

    for tipo, quantidade in sorted(contadores.items()):
        print(f"  {tipo}: {quantidade}")

# ============================================================================
# FUNÇÃO DE TESTE PARA lerTokens
# ============================================================================

def testarLerTokens():
    """
    Função de teste para demonstrar e validar a funcionalidade de lerTokens.
    """
    print("=== TESTE DA FUNÇÃO lerTokens ===")

    # Criar arquivo de teste temporário
    conteudo_teste = """# Teste de tokens para RA2
( 3 4 + )
( A B > IF X ELSE Y )
( 1 10 I FOR )
( X Y AND Z OR )
( A B == )
( COUNTER 5 <= WHILE )
RES
VAR MEM
"""

    arquivo_teste = "teste_tokens_temp.txt"

    try:
        # Escrever arquivo de teste
        with open(arquivo_teste, 'w', encoding='utf-8') as f:
            f.write(conteudo_teste)

        # Testar função lerTokens
        print(f"Lendo tokens do arquivo: {arquivo_teste}")
        tokens = lerTokens(arquivo_teste)

        print(f"\nTokens processados ({len(tokens)} total):")
        for i, token in enumerate(tokens, 1):
            print(f"  {i:2d}: {token}")

        # Validar tokens
        if validarTokens(tokens):
            print("\nValidação: Tokens estão corretos")
        else:
            print("\nValidação: Problemas encontrados nos tokens")

        # Exibir estatísticas
        exibirEstatisticasTokens(tokens)

        # Limpar arquivo temporário
        Path(arquivo_teste).unlink(missing_ok=True)

    except Exception as e:
        print(f"Erro durante teste: {e}")
        # Limpar arquivo temporário mesmo em caso de erro
        Path(arquivo_teste).unlink(missing_ok=True)

if __name__ == "__main__":
    """
    Execução direta do módulo para testes.
    """
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        print(f"Testando lerTokens com arquivo: {arquivo}")
        try:
            tokens = lerTokens(arquivo)
            print(f"Sucesso! {len(tokens)} tokens processados.")
            exibirEstatisticasTokens(tokens)
        except Exception as e:
            print(f"Erro: {e}")
    else:
        # Executar teste automatizado
        testarLerTokens()