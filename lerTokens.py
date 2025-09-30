#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import List, Optional

# Definições de Token para RA2 (baseadas na RA1 + extensões)
# Usando definições locais para evitar problemas de import

class Tipo_de_Token:
    
    NUMERO_REAL = "NUMERO_REAL"
    SOMA = "SOMA"                      # +
    SUBTRACAO = "SUBTRACAO"            # -
    MULTIPLICACAO = "MULT"             # *
    DIVISAO = "DIV"                    # / divisao inteira
    RESTO = "RESTO"                    # %
    POTENCIA = "POT"                   # ^
    ABRE_PARENTESES = "ABRE_PARENTESES" # (
    FECHA_PARENTESES = "FECHA_PARENTESES" # )
    RES = "RES"
    MEM = "MEM"
    FIM = "FIM"

    # Estruturas de controle
    FOR = "FOR"
    WHILE = "WHILE"
    IF = "IF"
    ELSE = "ELSE"
    ASSIGN = "ASSIGN"
    PRINT = "PRINT"

    # Operadores relacionais
    MAIOR = "MAIOR"                    # >
    MENOR = "MENOR"                    # <
    MAIOR_IGUAL = "MAIOR_IGUAL"        # >=
    MENOR_IGUAL = "MENOR_IGUAL"        # <=
    IGUAL = "IGUAL"                    # ==
    DIFERENTE = "DIFERENTE"            # !=

    # Fixed division operators (PORTUGUESE - matches RA1)
    DIVISAO_REAL = "DIVISAO_REAL"      # | (real division)
    # Keep DIVISAO = "DIV" for / (integer division)

    # Identifiers (PORTUGUESE - matches RA1 pattern)
    IDENTIFICADOR = "IDENTIFICADOR"    # Variable names

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
    Lê arquivo de tokens gerado na Fase 1 ou arquivo de código fonte para RA2.

    COMPATIBILIDADE RA1: Lê formato de saída da RA1 (tokens_gerados.txt)
    EXTENSÃO RA2: Lê código fonte com estruturas de controle

    Args:
        arquivo: Nome do arquivo (tokens da RA1 ou código fonte da RA2)

    Returns:
        Lista de tokens processados incluindo novos tokens de controle

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o formato dos tokens for inválido

    Formatos suportados:
        RA1: "3 2 +" (uma expressão RPN por linha)
        RA2: "( 3 2 + )" ou "( A B > IF X ELSE Y )" (estruturas de controle)
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
    tokens.append(Token(Tipo_de_Token.FIM, "$"))

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

    # ===== RA2 TOKEN RECOGNITION =====

    # Operadores relacionais
    if elemento == '>':
        return Token(Tipo_de_Token.MAIOR, elemento, linha, coluna)
    elif elemento == '<':
        return Token(Tipo_de_Token.MENOR, elemento, linha, coluna)
    elif elemento == '>=':
        return Token(Tipo_de_Token.MAIOR_IGUAL, elemento, linha, coluna)
    elif elemento == '<=':
        return Token(Tipo_de_Token.MENOR_IGUAL, elemento, linha, coluna)
    elif elemento == '==':
        return Token(Tipo_de_Token.IGUAL, elemento, linha, coluna)
    elif elemento == '!=':
        return Token(Tipo_de_Token.DIFERENTE, elemento, linha, coluna)

    # Estruturas de controle (separate IF and ELSE tokens)
    elif elemento == 'IF':
        return Token(Tipo_de_Token.IF, elemento, linha, coluna)
    elif elemento == 'ELSE':
        return Token(Tipo_de_Token.ELSE, elemento, linha, coluna)
    elif elemento == 'WHILE':
        return Token(Tipo_de_Token.WHILE, elemento, linha, coluna)
    elif elemento == 'FOR':
        return Token(Tipo_de_Token.FOR, elemento, linha, coluna)
    elif elemento == 'ASSIGN':
        return Token(Tipo_de_Token.ASSIGN, elemento, linha, coluna)
    elif elemento == 'PRINT':
        return Token(Tipo_de_Token.PRINT, elemento, linha, coluna)

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
        return Token(Tipo_de_Token.DIVISAO_REAL, elemento, linha, coluna)
    elif elemento == '/':  # Divisão inteira
        return Token(Tipo_de_Token.DIVISAO, elemento, linha, coluna)
    elif elemento == '%':  # Resto (módulo)
        return Token(Tipo_de_Token.RESTO, elemento, linha, coluna)
    elif elemento == '^':  # Potência
        return Token(Tipo_de_Token.POTENCIA, elemento, linha, coluna)

    # Comandos especiais
    elif elemento == 'RES':
        return Token(Tipo_de_Token.RES, elemento, linha, coluna)
    elif elemento.upper() == 'MEM':
        return Token(Tipo_de_Token.MEM, elemento, linha, coluna)
    elif elemento.isupper() and elemento.isalpha():
        # Identificadores (variáveis) - sequência de letras maiúsculas
        return Token(Tipo_de_Token.IDENTIFICADOR, elemento, linha, coluna)

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
                # Verificar se é identificador (variável)
                if elemento.isalpha():
                    return Token(Tipo_de_Token.IDENTIFICADOR, elemento, linha, coluna)
                # Token não reconhecido
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
        return False

    # Verificar se há parênteses balanceados
    contador_parenteses = 0
    for token in tokens:
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            contador_parenteses += 1
        elif token.tipo == Tipo_de_Token.FECHA_PARENTESES:
            contador_parenteses -= 1
            if contador_parenteses < 0:
                return False

    if contador_parenteses != 0:
        return False

    return True


# ============================================================================
# FUNÇÃO DE TESTE PARA lerTokens
# ============================================================================

def testarLerTokens():
    """
    Função de teste para demonstrar e validar a funcionalidade de lerTokens.
    """
    conteudo_teste = """# Teste de tokens para RA2
( 3 4 + )
( A B > IF X ELSE Y )
( 1 10 I FOR )
( A B == )
( A B == )
( COUNTER 5 <= WHILE )
RES
VAR MEM
"""

    arquivo_teste = "teste_tokens_temp.txt"

    try:
        with open(arquivo_teste, 'w', encoding='utf-8') as f:
            f.write(conteudo_teste)

        tokens = lerTokens(arquivo_teste)

        print(f"\n=== RETORNO DA FUNÇÃO lerTokens ===")
        print(f"Tipo do retorno: {type(tokens)}")
        print(f"Tokens processados: {len(tokens)}")
        print(f"\n=== LISTA DE TOKENS RETORNADA ===")
        for i, token in enumerate(tokens, 1):
            print(f"  {i:2d}: {token}")

        print(f"\n=== ESTRUTURA DOS OBJETOS TOKEN ===")
        if tokens:
            exemplo_token = tokens[0]
            print(f"Exemplo - Token[0]:")
            print(f"  .tipo: {exemplo_token.tipo}")
            print(f"  .valor: {exemplo_token.valor}")
            print(f"  .linha: {exemplo_token.linha}")
            print(f"  .coluna: {exemplo_token.coluna}")

        print(f"\n=== VALIDAÇÃO ===")
        if validarTokens(tokens):
            print("Validação: OK")
        else:
            print("Validação: Problemas encontrados")

        Path(arquivo_teste).unlink(missing_ok=True)

    except Exception as e:
        print(f"Erro durante teste: {e}")
        Path(arquivo_teste).unlink(missing_ok=True)

# ============================================================================
# TESTE INDEPENDENTE (sem main - apenas para desenvolvimento)
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        testarLerTokens()
    elif len(sys.argv) > 1:
        # Permitir testar com arquivo específico
        arquivo = sys.argv[1]
        try:
            print(f"=== TESTANDO COM ARQUIVO: {arquivo} ===")
            tokens = lerTokens(arquivo)
            print(f"Tokens processados: {len(tokens)}")
            print("Primeiros 10 tokens:")
            for i in range( len(tokens)):
                token = tokens[i]
                print(f"  {i+1:2d}: Token({token.tipo}, {token.valor})")

            if validarTokens(tokens):
                print("Validação: OK")
            else:
                print("Validação: Problemas encontrados")

        except Exception as e:
            print(f"Erro: {e}")
    else:
        print("Este arquivo contém apenas a implementação da função lerTokens.")
        print("Uso:")
        print("  python lerTokens.py --test           # Executar teste interno")
        print("  python lerTokens.py <arquivo>        # Testar com arquivo específico")
        print("  python lerTokens.py teste1.txt       # Exemplo")