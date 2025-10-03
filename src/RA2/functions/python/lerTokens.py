#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import sys
from pathlib import Path
from typing import List, Optional
from src.RA1.functions.python.tokens import Tipo_de_Token, Token

def lerTokens(arquivo: str) -> List[Token]:

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
    
    tokens = []
    
    # Usar análise caractere por caractere para capturar parênteses e elementos
    i = 0
    while i < len(linha):
        char = linha[i]
        
        # Pular espaços
        if char.isspace():
            i += 1
            continue
        
        # Processar parênteses individualmente
        if char == '(':
            token = reconhecerToken('(', linha_num, i)
            if token:
                tokens.append(token)
            i += 1
        elif char == ')':
            token = reconhecerToken(')', linha_num, i)
            if token:
                tokens.append(token)
            i += 1
        else:
            # Extrair elemento completo (número, variável, operador, palavra-chave)
            elemento = ''
            start_pos = i
            
            while i < len(linha) and not linha[i].isspace() and linha[i] not in '()':
                elemento += linha[i]
                i += 1
            
            if elemento:
                token = reconhecerToken(elemento, linha_num, start_pos)
                if token:
                    tokens.append(token)
    
    return tokens

def reconhecerToken(elemento: str, linha: int, coluna: int) -> Optional[Token]:

    # Tratar elemento vazio
    if not elemento:
        return None
    
    # ===== SÍMBOLOS DE AGRUPAMENTO =====
    if elemento == '(':
        return Token(Tipo_de_Token.ABRE_PARENTESES, elemento)
    elif elemento == ')':
        return Token(Tipo_de_Token.FECHA_PARENTESES, elemento)
    
    # ===== ESTRUTURAS DE CONTROLE =====
    elif elemento == 'IFELSE':
        return Token(Tipo_de_Token.IFELSE, elemento)
    elif elemento == 'WHILE':
        return Token(Tipo_de_Token.WHILE, elemento)
    elif elemento == 'FOR':
        return Token(Tipo_de_Token.FOR, elemento)
    
    # ===== COMANDOS ESPECIAIS =====
    elif elemento == 'RES':
        return Token(Tipo_de_Token.RES, elemento)
    
    # ===== OPERADORES RELACIONAIS =====
    elif elemento == '>=':
        return Token(Tipo_de_Token.MAIOR_IGUAL, elemento)
    elif elemento == '<=':
        return Token(Tipo_de_Token.MENOR_IGUAL, elemento)
    elif elemento == '==':
        return Token(Tipo_de_Token.IGUAL, elemento)
    elif elemento == '!=':
        return Token(Tipo_de_Token.DIFERENTE, elemento)
    elif elemento == '||':
        return Token(Tipo_de_Token.OR, elemento)
    elif elemento == '&&':
        return Token(Tipo_de_Token.AND, elemento)
    elif elemento == '>':
        return Token(Tipo_de_Token.MAIOR, elemento)
    elif elemento == '<':
        return Token(Tipo_de_Token.MENOR, elemento)
    
    # ===== OPERADORES ARITMÉTICOS =====
    elif elemento == '+':
        return Token(Tipo_de_Token.SOMA, elemento)
    elif elemento == '-':
        return Token(Tipo_de_Token.SUBTRACAO, elemento)
    elif elemento == '*':
        return Token(Tipo_de_Token.MULTIPLICACAO, elemento)
    elif elemento == '/':
        return Token(Tipo_de_Token.DIVISAO, elemento)
    elif elemento == '%':
        return Token(Tipo_de_Token.RESTO, elemento)
    elif elemento == '^':
        return Token(Tipo_de_Token.POTENCIA, elemento)
    
    # ===== OPERADORES LÓGICOS =====
    elif elemento == '!':
        return Token(Tipo_de_Token.NOT, elemento)
    
    # ===== NÚMEROS =====
    else:
        # Verificar se é número (inteiro ou real)
        try:
            # Primeiro tentar como float (inclui inteiros)
            float(elemento)
            return Token(Tipo_de_Token.NUMERO_REAL, elemento)
        except ValueError:
            # Se não é número, então é uma variável
            # Qualquer coisa que não seja um token específico é considerada variável
            return Token(Tipo_de_Token.VARIAVEL, elemento)

def lerTokensDoArquivo(arquivo_tokens: str) -> List[Token]:
    """
    Le arquivo de tokens gerado pelo RA1 (outputs/RA1/tokens/tokens_gerados.txt).

    Formato esperado: cada linha contem tokens separados por espaco
    Exemplo: "( 3.0 2.0 + )"

    Args:
        arquivo_tokens: Caminho para o arquivo de tokens do RA1

    Returns:
        Lista de objetos Token processados de todas as linhas

    Raises:
        FileNotFoundError: Se arquivo nao existe
    """
    tokens = []

    try:
        with open(arquivo_tokens, 'r', encoding='utf-8') as f:
            for linha_num, linha in enumerate(f, 1):
                linha = linha.strip()

                # Pular linhas vazias e comentarios
                if not linha or linha.startswith('#'):
                    continue

                # Processar tokens da linha (mesma logica de processarLinha)
                tokens_linha = processarLinha(linha, linha_num)
                tokens.extend(tokens_linha)

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de tokens nao encontrado: {arquivo_tokens}")
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo de tokens: {e}")

    # Adicionar token de fim de arquivo
    tokens.append(Token(Tipo_de_Token.FIM, "$"))

    return tokens


def validarTokens(tokens: List[Token]) -> bool:
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