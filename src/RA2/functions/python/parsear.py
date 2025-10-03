#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

from typing import List, Dict, Tuple, Optional
from src.RA1.functions.python.tokens import Token
from .configuracaoGramatica import SIMBOLO_INICIAL, MAPEAMENTO_TOKENS

def parsear(tabela_ll1: Dict, tokens_linha: List[Token]) -> List[str]:
    
    if not tokens_linha:
        return []
    
    # Mapear tokens para símbolos que a tabela LL(1) espera
    entrada = []
    for token in tokens_linha:
        # Verificar se é número
        try:
            float(token.valor)
            entrada.append(MAPEAMENTO_TOKENS['NUMERO_REAL'])  # 'NUMBER'
        except ValueError:
            # Verificar se é variável (uma letra A-Z)
            if len(token.valor) == 1 and token.valor.isalpha() and token.valor.isupper():
                entrada.append(MAPEAMENTO_TOKENS['VARIAVEL'])  # 'IDENTIFIER'
            # Usar mapeamento existente para outros tokens
            else:
                # Buscar no mapeamento reverso
                token_mapeado = None
                for teorico, real in MAPEAMENTO_TOKENS.items():
                    if real == token.valor:
                        token_mapeado = real
                        break
                entrada.append(token_mapeado if token_mapeado else MAPEAMENTO_TOKENS['VARIAVEL'])
    entrada.append('$')  # Símbolo de fim de cadeia
    
    # Inicializa pilha e índice de entrada
    pilha = ['$', SIMBOLO_INICIAL]
    indice = 0
    derivacao = []
    
    try:
        while len(pilha) > 1:  # Enquanto a pilha não contém apenas '$'
            topo = pilha[-1]
            simbolo_entrada = entrada[indice] if indice < len(entrada) else '$'
            
            # Se o topo da pilha é terminal
            if topo == simbolo_entrada:
                pilha.pop()
                indice += 1
                continue
            
            # Se o topo da pilha é não-terminal, busca na tabela
            if topo not in tabela_ll1:
                return []
            
            if simbolo_entrada not in tabela_ll1[topo]:
                return []
            
            producao = tabela_ll1[topo][simbolo_entrada]
            
            if producao is None:
                return []
            
            # Remove o não-terminal da pilha
            pilha.pop()
            
            # Adiciona a produção à derivação
            if producao == ['EPSILON']:
                derivacao.append(f"{topo} → ε")
            else:
                # Mapear produção para símbolos teóricos usando mapeamento reverso
                producao_teorica = []
                for simbolo in producao:
                    # Buscar mapeamento reverso
                    simbolo_teorico = None
                    for teorico, real in MAPEAMENTO_TOKENS.items():
                        if real == simbolo:
                            simbolo_teorico = teorico
                            break
                    producao_teorica.append(simbolo_teorico if simbolo_teorico else simbolo)
                        
                derivacao.append(f"{topo} → {' '.join(producao_teorica)}")
                
                # Adiciona os símbolos da produção à pilha (ordem inversa)
                for simbolo in reversed(producao):
                    if simbolo != 'EPSILON':
                        pilha.append(simbolo)
        
        # Verifica se toda a entrada foi consumida
        if indice == len(entrada) - 1 and entrada[indice] == '$':
            return derivacao
        else:
            return []
            
    except Exception:
        return []

def parsear_todas_linhas(tabela_ll1: Dict, tokens_por_linha: List[List[Token]]) -> List[List[str]]:
    
    derivacoes = []
    
    for i, tokens_linha in enumerate(tokens_por_linha):
        print(f"Processando linha {i+1}: {[t.valor for t in tokens_linha]}")
        
        derivacao = parsear(tabela_ll1, tokens_linha)
        
        if derivacao:
            print(f"    Derivação gerada com {len(derivacao)} passos")
            derivacoes.append(derivacao)
        else:
            print(f"    Erro sintático - linha rejeitada")
            # Adiciona derivação vazia para manter indexação
            derivacoes.append([])
    
    return derivacoes

