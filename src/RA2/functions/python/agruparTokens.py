#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Integrantes do grupo (ordem alfabetica):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenco Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from typing import List
from src.RA1.functions.python.tokens import Token, Tipo_de_Token


def agrupar_tokens_por_expressao(tokens: List[Token]) -> List[List[Token]]:
    """
    Agrupa tokens em expressoes individuais baseado em parenteses balanceados.

    Cada expressao comeca com '(' e termina quando os parenteses estao balanceados.

    Args:
        tokens: Lista completa de tokens do arquivo

    Returns:
        Lista de listas, onde cada sublista contem tokens de uma expressao completa

    Exemplo:
        Input:  [(, 3, 2, +, ), (, 5, MEM, ), $]
        Output: [[(, 3, 2, +, )], [(, 5, MEM, )]]
    """
    expressoes = []
    expressao_atual = []
    contador_parenteses = 0

    for token in tokens:
        # Ignora token FIM no processamento
        if token.tipo == Tipo_de_Token.FIM:
            continue

        # Adiciona token a expressao atual
        expressao_atual.append(token)

        # Conta parenteses
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            contador_parenteses += 1
        elif token.tipo == Tipo_de_Token.FECHA_PARENTESES:
            contador_parenteses -= 1

            # Quando parenteses estao balanceados, expressao completa
            if contador_parenteses == 0 and len(expressao_atual) > 0:
                # Adiciona token FIM ao final da expressao
                expressao_atual.append(Token(Tipo_de_Token.FIM, "$"))
                expressoes.append(expressao_atual)
                expressao_atual = []

    # Se sobrou expressao incompleta, adiciona mesmo assim
    if len(expressao_atual) > 0:
        expressao_atual.append(Token(Tipo_de_Token.FIM, "$"))
        expressoes.append(expressao_atual)

    return expressoes


def extrair_texto_expressao(tokens: List[Token]) -> str:
    """
    Extrai o texto original da expressao a partir dos tokens.

    Args:
        tokens: Lista de tokens de uma expressao

    Returns:
        String com a expressao original (ex: "(3 2 +)")
    """
    partes = []
    for token in tokens:
        if token.tipo != Tipo_de_Token.FIM:
            partes.append(str(token.valor))

    return ' '.join(partes)
