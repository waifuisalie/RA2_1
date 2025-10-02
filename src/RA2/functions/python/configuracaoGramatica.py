#!/usr/bin/env python3

# Símbolo inicial da gramática (constante)
SIMBOLO_INICIAL = 'PROGRAMA'

# Definição da gramática RPN (constante)
GRAMATICA_RPN = {
    # Símbolo inicial - programa completo
    'PROGRAMA': [['LINHA_LIST']],
    
    # Lista de linhas - pode ter múltiplas linhas ou ser vazia
    'LINHA_LIST': [
        ['LINHA', 'LINHA_LIST'],  # Uma linha seguida de mais linhas
        ['EPSILON']               # Lista vazia (fim do programa)
    ],
    
    # Cada linha é uma expressão completa entre parênteses
    'LINHA': [['(', 'CONTEUDO', ')']],
    
    # Conteúdo da linha - diferenciado por primeira palavra (LL(1) friendly)
    'CONTEUDO': [
        # Estruturas de controle (palavras-chave únicas)
        ['IFELSE', 'CONDICAO', 'EXPRESSAO', 'EXPRESSAO'],           # (IFELSE cond then else)
        ['WHILE', 'CONDICAO', 'EXPRESSAO'],                        # (WHILE cond body)
        ['FOR', 'EXPRESSAO', 'EXPRESSAO', 'EXPRESSAO', 'EXPRESSAO'], # (FOR start end step body)
        
        # Operações específicas
        ['NUMBER', 'RES'],                                         # (5 RES)
        ['NUMBER', 'IDENTIFIER'],                                  # (5.5 A) - atribuição
        ['IDENTIFIER', 'IDENTIFIER'],                              # (A B) - possível erro, mas precisa estar
        
        # Operações binárias - começam com operando
        ['NUMBER', 'NUMBER', 'OPERADOR'],                         # (3 4 +)
        ['NUMBER', 'IDENTIFIER', 'OPERADOR'],                     # (3 A +)
        ['IDENTIFIER', 'NUMBER', 'OPERADOR'],                     # (A 3 +)  
        ['IDENTIFIER', 'IDENTIFIER', 'OPERADOR'],                 # (A B +)
        ['(', 'CONTEUDO', ')', 'OPERANDO', 'OPERADOR'],          # ((A B +) C *)
        ['OPERANDO', '(', 'CONTEUDO', ')', 'OPERADOR'],          # (A (B C +) *)
        ['(', 'CONTEUDO', ')', '(', 'CONTEUDO', ')', 'OPERADOR'] # ((A B +) (C D *) /)
    ],
    
    # Condições para estruturas de controle
    'CONDICAO': [
        ['(', 'OPERANDO', 'OPERANDO', 'COMPARADOR', ')'],                    # (A B >)
        ['(', '(', 'OPERANDO', 'OPERANDO', 'COMPARADOR', ')', 
         '(', 'OPERANDO', 'OPERANDO', 'COMPARADOR', ')', 'OPERADOR_LOGICO', ')'] # ((A B >) (C D <=) &&)
    ],
    
    # Expressões para corpo de estruturas de controle
    'EXPRESSAO': [
        ['(', 'CONTEUDO', ')']    # Expressão é sempre uma linha completa
    ],
    
    # Operandos básicos
    'OPERANDO': [
        ['NUMBER'],               # Números: 5.5, 3.2, etc.
        ['IDENTIFIER'],           # Variáveis: A, B, X, etc.
        ['(', 'CONTEUDO', ')']    # Expressões aninhadas
    ],
    
    # Operadores aritméticos
    'OPERADOR': [
        ['+'], ['-'], ['*'], ['/'], ['%'], ['^']
    ],
    
    # Operadores de comparação
    'COMPARADOR': [
        ['<'], ['>'], ['<='], ['>='], ['=='], ['!=']
    ],
    
    # Operadores lógicos
    'OPERADOR_LOGICO': [
        ['&&'], ['||'], ['!']
    ]
}