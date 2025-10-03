#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

# Símbolo inicial da gramática corrigida
SIMBOLO_INICIAL = 'PROGRAM'

GRAMATICA_RPN = {
    # Programa principal
    'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
    'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['EPSILON']],
    
    # Estrutura de linha
    'LINHA': [['ABRE_PARENTESES', 'CONTENT', 'FECHA_PARENTESES']],
    
    # Conteúdo principal - diferenciado deterministicamente
    'CONTENT': [
        ['NUMERO_REAL', 'AFTER_NUM'],
        ['VARIAVEL', 'AFTER_VAR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],
        ['FOR', 'FOR_STRUCT'],
        ['WHILE', 'WHILE_STRUCT'],
        ['IFELSE', 'IFELSE_STRUCT']
    ],
    
    # AFTER_NUM - processar após número inicial
    'AFTER_NUM': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'AFTER_VAR_OP'],  # INOVAÇÃO: Continuação não-terminal
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR'],
        ['NOT'],  # Suporte para operador unário NOT
        ['RES'],
        ['EPSILON']  # Para permitir fechamento direto como em (5)
    ],
    
    'AFTER_VAR_OP': [['OPERATOR'], ['EPSILON']],
    
    # AFTER_VAR - processar após variável inicial  
    'AFTER_VAR': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'AFTER_VAR_OP'],  # Permite variável sem operador obrigatório
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR'],
        ['NOT'],  # Suporte para operador unário NOT
        ['EPSILON']
    ],
    
    # AFTER_EXPR - processar após expressão em parênteses
    'AFTER_EXPR': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'AFTER_VAR_OP'],  # Usa mesma estratégia de AFTER_NUM
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],  # Permite expr recursiva
        ['OPERATOR', 'EXPR_CHAIN'],  # Para operadores seguidos de mais expressões
        ['EPSILON']    # Para permitir fechamento direto
    ],
    
    # EXPR_CHAIN - para operadores entre expressões
    'EXPR_CHAIN': [
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],
        ['EPSILON']
    ],
    
    # EXPR - expressões internas
    'EXPR': [
        ['NUMERO_REAL', 'AFTER_NUM'],
        ['VARIAVEL', 'AFTER_VAR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],
        ['IFELSE', 'IFELSE_STRUCT']  # Permite IFELSE em expressões
    ],
    
    # Hierarquia de operadores
    'OPERATOR': [['ARITH_OP'], ['COMP_OP'], ['LOGIC_OP']],
        'ARITH_OP': [['SOMA'], ['SUBTRACAO'], ['MULTIPLICACAO'], ['DIVISAO_INTEIRA'], ['DIVISAO_REAL'], ['RESTO'], ['POTENCIA']],
    'COMP_OP': [['MENOR'], ['MAIOR'], ['IGUAL'], ['MENOR_IGUAL'], ['MAIOR_IGUAL'], ['DIFERENTE']],
    'LOGIC_OP': [['AND'], ['OR'], ['NOT']],
    
    # Estruturas de controle
    'FOR_STRUCT': [['ABRE_PARENTESES', 'NUMERO_REAL', 'FECHA_PARENTESES', 
                   'ABRE_PARENTESES', 'NUMERO_REAL', 'FECHA_PARENTESES', 
                   'ABRE_PARENTESES', 'NUMERO_REAL', 'FECHA_PARENTESES', 'LINHA']],
    'WHILE_STRUCT': [['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'LINHA']],
    'IFELSE_STRUCT': [['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'LINHA', 'LINHA']]
}

# Mapeamento dos tokens teóricos para tokens reais do projeto
MAPEAMENTO_TOKENS = {
    'NUMERO_REAL': 'NUMBER',
    'VARIAVEL': 'IDENTIFIER', 
    'ABRE_PARENTESES': '(',
    'FECHA_PARENTESES': ')',
    'SOMA': '+',
    'SUBTRACAO': '-',
    'MULTIPLICACAO': '*',
    'DIVISAO_INTEIRA': '/',
    'DIVISAO_REAL': '|',
    'RESTO': '%',
    'POTENCIA': '^',
    'MENOR': '<',
    'MAIOR': '>',
    'IGUAL': '==',
    'MENOR_IGUAL': '<=',
    'MAIOR_IGUAL': '>=',
    'DIFERENTE': '!=',
    'AND': '&&',
    'OR': '||',
    'NOT': '!',
    'FOR': 'FOR',
    'WHILE': 'WHILE',
    'IFELSE': 'IFELSE',
    'RES': 'RES'
}

# ============================================================================
# FUNÇÕES DE MAPEAMENTO - Centralizadas para evitar duplicação
# ============================================================================

def mapear_gramatica_para_tokens_reais(gramatica_teorica):
    """Converte gramática com tokens teóricos para tokens reais do projeto"""
    gramatica_real = {}
    
    for nt, producoes in gramatica_teorica.items():
        gramatica_real[nt] = []
        for producao in producoes:
            producao_real = []
            for simbolo in producao:
                # Se é um token teórico, mapeia para o real
                if simbolo in MAPEAMENTO_TOKENS:
                    producao_real.append(MAPEAMENTO_TOKENS[simbolo])
                else:
                    producao_real.append(simbolo)
            gramatica_real[nt].append(producao_real)
    
    return gramatica_real

def mapear_tokens_reais_para_teoricos(conjunto_ou_dict):
    """Converte tokens reais de volta para tokens teóricos para exibição"""
    # Cria mapeamento inverso
    mapeamento_inverso = {v: k for k, v in MAPEAMENTO_TOKENS.items()}
    
    if isinstance(conjunto_ou_dict, set):
        # Para conjuntos FIRST/FOLLOW
        return {mapeamento_inverso.get(token, token) for token in conjunto_ou_dict}
    elif isinstance(conjunto_ou_dict, dict):
        # Para tabela LL(1) 
        resultado = {}
        for nt, terminais_dict in conjunto_ou_dict.items():
            resultado[nt] = {}
            for terminal, producao in terminais_dict.items():
                terminal_teorico = mapeamento_inverso.get(terminal, terminal)
                if producao is not None:
                    # Mapear tokens na produção de volta para teóricos
                    producao_teorica = [mapeamento_inverso.get(simbolo, simbolo) for simbolo in producao]
                    resultado[nt][terminal_teorico] = producao_teorica
                else:
                    resultado[nt][terminal_teorico] = None
        return resultado
    else:
        return conjunto_ou_dict