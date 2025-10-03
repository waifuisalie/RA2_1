#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Integrantes do grupo (ordem alfabetica):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenco Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from typing import List, Dict, Optional
from src.RA1.functions.python.tokens import Token, Tipo_de_Token

class ErroSintatico(Exception):
    """Excecao personalizada para erros sintaticos durante o parsing"""
    pass


def mapear_token_para_gramatica(token: Token) -> str:
    """
    Mapeia tokens do analisador lexico para os simbolos da gramatica/tabela LL(1).

    Args:
        token: Token do analisador lexico

    Returns:
        String representando o simbolo na gramatica
    """
    # Mapeamento direto de Tipo_de_Token para simbolos da gramatica
    mapeamento = {
        Tipo_de_Token.NUMERO_REAL: "NUMBER",
        Tipo_de_Token.VARIAVEL: "IDENTIFIER",
        Tipo_de_Token.ABRE_PARENTESES: "(",
        Tipo_de_Token.FECHA_PARENTESES: ")",
        Tipo_de_Token.SOMA: "+",
        Tipo_de_Token.SUBTRACAO: "-",
        Tipo_de_Token.MULTIPLICACAO: "*",
        Tipo_de_Token.DIVISAO: "/",
        Tipo_de_Token.RESTO: "%",
        Tipo_de_Token.POTENCIA: "^",
        Tipo_de_Token.MENOR: "<",
        Tipo_de_Token.MAIOR: ">",
        Tipo_de_Token.IGUAL: "==",
        Tipo_de_Token.MENOR_IGUAL: "<=",
        Tipo_de_Token.MAIOR_IGUAL: ">=",
        Tipo_de_Token.DIFERENTE: "!=",
        Tipo_de_Token.AND: "&&",
        Tipo_de_Token.OR: "||",
        Tipo_de_Token.NOT: "!",
        Tipo_de_Token.FOR: "FOR",
        Tipo_de_Token.WHILE: "WHILE",
        Tipo_de_Token.IFELSE: "IFELSE",
        Tipo_de_Token.RES: "RES",
        Tipo_de_Token.FIM: "$"
    }

    return mapeamento.get(token.tipo, token.valor)


def eh_nao_terminal(simbolo: str) -> bool:
    """
    Verifica se um simbolo eh nao-terminal (maiusculas e underscores).

    Args:
        simbolo: String representando o simbolo

    Returns:
        True se for nao-terminal, False caso contrario
    """
    if not simbolo or simbolo == "$":
        return False

    # Lista de terminais conhecidos (tokens reais da tabela LL1)
    terminais = {
        '(', ')', '+', '-', '*', '/', '%', '^',
        '<', '>', '==', '<=', '>=', '!=',
        '&&', '||', '!',
        'FOR', 'WHILE', 'IFELSE', 'RES',
        'NUMBER', 'IDENTIFIER'
    }

    if simbolo in terminais:
        return False

    # Nao-terminais sao compostos apenas de letras maiusculas e underscores
    return simbolo.replace("_", "").isupper()


def parsear(tokens: List[Token], tabela_ll1: Dict[str, Dict[str, Optional[List[str]]]], simbolo_inicial: str = 'PROGRAM', verbose: bool = True) -> List[str]:
    """
    Parser LL(1) table-driven que analisa sintatica de tokens usando tabela LL(1).

    Algoritmo:
    1. Inicializa pilha com ['$', simbolo_inicial]
    2. Para cada token de entrada:
       - Se topo = token: desempilha e avanca token (match)
       - Se topo eh nao-terminal: consulta tabela LL(1), aplica producao
       - Se topo = EPSILON: desempilha sem consumir token
    3. Sucesso quando pilha e entrada = '$'

    Args:
        tokens: Lista de tokens do analisador lexico (deve terminar com Token.FIM/$)
        tabela_ll1: Tabela LL(1) com estrutura {nao_terminal: {terminal: producao}}
                    onde producao eh lista de simbolos ou None
        simbolo_inicial: Simbolo inicial da gramatica (default: 'PROGRAM')
        verbose: Se True, imprime debug do parsing (default: True)

    Returns:
        Lista de strings representando a derivacao mais a esquerda
        Exemplo: ['PROGRAM -> LINHA PROGRAM_PRIME', 'LINHA -> ( CONTENT )', ...]

    Raises:
        ErroSintatico: Quando encontra erro sintatico (token inesperado, producao nao definida)
    """

    # Verifica se ha tokens
    if not tokens:
        raise ErroSintatico("Lista de tokens vazia")

    # Garante que ultimo token eh FIM/$
    if tokens[-1].tipo != Tipo_de_Token.FIM:
        tokens.append(Token(Tipo_de_Token.FIM, "$"))

    # Inicializacao
    pilha = ['$', simbolo_inicial]  # Topo a direita
    indice_token = 0
    derivacao = []

    if verbose:
        print("\n=== INICIANDO PARSING LL(1) ===")
        print(f"Tokens de entrada: {len(tokens)} tokens")
        print(f"Simbolo inicial: {simbolo_inicial}\n")

    passo = 0

    # Loop principal do parser
    while len(pilha) > 0:
        passo += 1
        topo = pilha[-1]  # Topo da pilha (ultima posicao)
        token_atual = tokens[indice_token]
        simbolo_entrada = mapear_token_para_gramatica(token_atual)

        # Debug: mostrar estado atual
        if verbose:
            pilha_str = ' '.join(pilha)
            print(f"Passo {passo:3d} | Pilha: [{pilha_str}]")
            print(f"          | Topo: {topo:20s} | Token: {token_atual.valor:10s} ({simbolo_entrada})")

        # CASO 1: Sucesso - pilha e entrada sao '$'
        if topo == '$' and simbolo_entrada == '$':
            if verbose:
                print("\n[OK] PARSING CONCLUIDO COM SUCESSO!\n")
            break

        # CASO 2: Terminal no topo - deve fazer match com token
        if not eh_nao_terminal(topo):
            if topo == simbolo_entrada:
                if verbose:
                    print(f"          -> Match: '{topo}' == '{simbolo_entrada}' [OK]")
                pilha.pop()
                indice_token += 1
            else:
                raise ErroSintatico(
                    f"\nErro sintatico no passo {passo}!\n"
                    f"  Token esperado: '{topo}'\n"
                    f"  Token encontrado: '{token_atual.valor}' ({simbolo_entrada})\n"
                    f"  Posicao: token {indice_token + 1}\n"
                    f"  Pilha: {pilha_str}"
                )

        # CASO 3: Nao-terminal no topo - consultar tabela LL(1)
        else:
            # Verifica se nao-terminal existe na tabela
            if topo not in tabela_ll1:
                raise ErroSintatico(
                    f"\nErro interno: nao-terminal '{topo}' nao encontrado na tabela LL(1)"
                )

            # Verifica se ha producao para [topo, simbolo_entrada]
            if simbolo_entrada not in tabela_ll1[topo]:
                raise ErroSintatico(
                    f"\nErro sintatico no passo {passo}!\n"
                    f"  Nao-terminal: {topo}\n"
                    f"  Token nao esperado: '{token_atual.valor}' ({simbolo_entrada})\n"
                    f"  Posicao: token {indice_token + 1}\n"
                    f"  Tokens validos para {topo}: {list(tabela_ll1[topo].keys())}"
                )

            producao = tabela_ll1[topo][simbolo_entrada]

            if producao is None:
                raise ErroSintatico(
                    f"\nErro sintatico no passo {passo}!\n"
                    f"  Producao nao definida: M[{topo}, {simbolo_entrada}]\n"
                    f"  Token: '{token_atual.valor}'\n"
                    f"  Posicao: token {indice_token + 1}"
                )

            # Desempilha nao-terminal
            pilha.pop()

            # Aplica producao (empilha da direita para esquerda, exceto EPSILON)
            if producao != ['EPSILON']:
                # Empilha simbolos na ordem reversa (direita -> esquerda)
                for simbolo in reversed(producao):
                    pilha.append(simbolo)
                producao_str = ' '.join(producao)
            else:
                producao_str = 'EPSILON'

            # Registra na derivacao
            derivacao_str = f"{topo} -> {producao_str}"
            derivacao.append(derivacao_str)

            if verbose:
                print(f"          -> Aplicando: {derivacao_str}")

        if verbose:
            print()  # Linha em branco entre passos

    if verbose:
        print(f"Total de passos: {passo}")
        print(f"Tokens consumidos: {indice_token}/{len(tokens)}")
        print(f"Producoes aplicadas: {len(derivacao)}\n")

    return derivacao
