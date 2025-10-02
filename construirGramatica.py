# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

"""
construirGramatica.py - ALUNO 1
================================
Implementa APENAS a gramática LL(1) e suas funções auxiliares.
NÃO inclui analisador léxico ou funções de token (já existem na Fase 1).
"""

from typing import Dict, Set, List, Tuple

# ============================================================================
# DEFINIÇÃO DA GRAMÁTICA
# ============================================================================

def definir_gramatica() -> Dict[str, List[List[str]]]:
    """
    Define as 45 regras de produção da gramática RPN com símbolos literais.
    
    Returns:
        Dict com não-terminais como chaves e lista de produções como valores
    """
    gramatica = {
    # Regras 1-3: Estrutura do programa
    'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
    'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['EPSILON']],
    
    # Regra 4: Linha
    'LINHA': [['ABRE_PARENTESES', 'CONTENT', 'FECHA_PARENTESES']],
    
    # Regras 5-10: Conteúdo
    'CONTENT': [
        ['NUMERO_REAL', 'AFTER_NUM'],
        ['VARIAVEL', 'AFTER_VAR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],
        ['FOR', 'FOR_STRUCT'],
        ['WHILE', 'WHILE_STRUCT'],
        ['IFELSE', 'IFELSE_STRUCT']
    ],
    
    # Regras 11-14: Depois de NUMERO_REAL
    'AFTER_NUM': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'OPERATOR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR'],
        ['RES']
    ],
    
    # Regras 15-18: Depois de VARIAVEL
    'AFTER_VAR': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'OPERATOR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR'],
        ['EPSILON']
    ],
    
    # Regras 19-21: Depois de expressão aninhada
    'AFTER_EXPR': [
        ['NUMERO_REAL', 'OPERATOR'],
        ['VARIAVEL', 'OPERATOR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR']
    ],
    
    # Regras 22-24: Expressão recursiva
    'EXPR': [
        ['NUMERO_REAL', 'AFTER_NUM'],
        ['VARIAVEL', 'AFTER_VAR'],
        ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR']
    ],
    
    # Regras 25-27: Operadores (agrupamento)
    'OPERATOR': [['ARITH_OP'], ['COMP_OP'], ['LOGIC_OP']],
    
    # Regras 28-33: Operadores aritméticos
    'ARITH_OP': [
        ['SOMA'],
        ['SUBTRACAO'],
        ['MULTIPLICACAO'],
        ['DIVISAO'],
        ['RESTO'],
        ['POTENCIA']
    ],
    
    # Regras 34-39: Operadores relacionais
    'COMP_OP': [
        ['MENOR'],
        ['MAIOR'],
        ['IGUAL'],
        ['MENOR_IGUAL'],
        ['MAIOR_IGUAL'],
        ['DIFERENTE']
    ],
    
    # Regras 40-42: Operadores lógicos
    'LOGIC_OP': [
        ['AND'],
        ['OR'],
        ['NOT']
    ],
    
    # Regra 43: Estrutura FOR
    'FOR_STRUCT': [['NUMERO_REAL', 'NUMERO_REAL', 'VARIAVEL', 'LINHA']],
    
    # Regra 44: Estrutura WHILE
    'WHILE_STRUCT': [['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'LINHA']],
    
    # Regra 45: Estrutura IFELSE
    'IFELSE_STRUCT': [['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'LINHA', 'LINHA']]
}

    
    return gramatica


def obter_terminais() -> Set[str]:
    """
    Retorna o conjunto de todos os símbolos terminais da gramática.
    Usa símbolos literais conforme especificado.
    """
    return {
        # Delimitadores
        '(', ')',
        
        # Literais
        'NUMBER', 'IDENTIFIER',
        
        # Operadores aritméticos
        '+', '-', '*', '|', '/', '%', '^',
        
        # Operadores relacionais
        '>', '<', '==', '!=', '>=', '<=',
        
        # Operadores lógicos
        '&&', '||', '!',
        
        # Comandos especiais
        'MEM', 'RES',
        
        # Estruturas de controle
        'FOR', 'WHILE', 'IF', 'ELSE',
        
        # Especiais
        'EPSILON', 'EOF'
    }


def obter_nao_terminais(gramatica: Dict) -> Set[str]:
    """Retorna o conjunto de todos os não-terminais da gramática"""
    return set(gramatica.keys())


# ============================================================================
# CÁLCULO DOS CONJUNTOS FIRST
# ============================================================================

def calcularFirst(gramatica: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
    """
    Calcula o conjunto FIRST para cada não-terminal da gramática.
    
    FIRST(X) = conjunto de terminais que podem aparecer no início de 
               strings derivadas de X
    
    Args:
        gramatica: Dicionário com as regras de produção
        
    Returns:
        Dicionário com conjuntos FIRST de cada símbolo
    """
    terminais = obter_terminais()
    nao_terminais = obter_nao_terminais(gramatica)
    
    # Inicializar FIRST vazio para cada não-terminal
    first = {nt: set() for nt in nao_terminais}
    
    # Adicionar FIRST dos terminais (o próprio terminal)
    for terminal in terminais:
        first[terminal] = {terminal}
    
    # Iteração até ponto fixo (até não haver mais mudanças)
    mudou = True
    while mudou:
        mudou = False
        
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                # Se produção é epsilon
                if producao[0] == 'EPSILON':
                    if 'EPSILON' not in first[nao_terminal]:
                        first[nao_terminal].add('EPSILON')
                        mudou = True
                    continue
                
                # Para cada símbolo na produção
                for i, simbolo in enumerate(producao):
                    # Obter FIRST do símbolo
                    if simbolo in terminais:
                        simbolo_first = {simbolo}
                    else:
                        simbolo_first = first[simbolo].copy()
                    
                    # Adicionar FIRST(simbolo) - {ε} a FIRST(nao_terminal)
                    antes = len(first[nao_terminal])
                    first[nao_terminal] |= (simbolo_first - {'EPSILON'})
                    if len(first[nao_terminal]) > antes:
                        mudou = True
                    
                    # Se ε não está em FIRST(simbolo), parar
                    if 'EPSILON' not in simbolo_first:
                        break
                    
                    # Se chegou ao último símbolo e todos têm ε, adicionar ε
                    if i == len(producao) - 1:
                        if 'EPSILON' not in first[nao_terminal]:
                            first[nao_terminal].add('EPSILON')
                            mudou = True
    
    return first


# ============================================================================
# CÁLCULO DOS CONJUNTOS FOLLOW
# ============================================================================

def calcularFollow(gramatica: Dict[str, List[List[str]]], 
                   first: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Calcula o conjunto FOLLOW para cada não-terminal da gramática.
    
    FOLLOW(X) = conjunto de terminais que podem aparecer imediatamente 
                após X em alguma derivação
    
    Args:
        gramatica: Dicionário com as regras de produção
        first: Conjuntos FIRST calculados anteriormente
        
    Returns:
        Dicionário com conjuntos FOLLOW de cada não-terminal
    """
    nao_terminais = obter_nao_terminais(gramatica)
    terminais = obter_terminais()
    
    # Inicializar FOLLOW vazio para cada não-terminal
    follow = {nt: set() for nt in nao_terminais}
    
    # Adicionar EOF ao FOLLOW do símbolo inicial
    follow['PROGRAM'].add('EOF')
    
    # Iteração até ponto fixo
    mudou = True
    while mudou:
        mudou = False
        
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                # Ignorar epsilon
                if producao[0] == 'EPSILON':
                    continue
                
                # Para cada símbolo não-terminal na produção
                for i, simbolo in enumerate(producao):
                    if simbolo not in nao_terminais:
                        continue
                    
                    # Símbolos após o atual
                    resto = producao[i + 1:]
                    
                    if not resto:
                        # Último símbolo: FOLLOW(simbolo) += FOLLOW(nao_terminal)
                        antes = len(follow[simbolo])
                        follow[simbolo] |= follow[nao_terminal]
                        if len(follow[simbolo]) > antes:
                            mudou = True
                    else:
                        # Calcular FIRST do resto
                        first_resto = set()
                        todos_tem_epsilon = True
                        
                        for prox_simbolo in resto:
                            if prox_simbolo in terminais:
                                first_resto.add(prox_simbolo)
                                todos_tem_epsilon = False
                                break
                            else:
                                first_resto |= (first[prox_simbolo] - {'EPSILON'})
                                if 'EPSILON' not in first[prox_simbolo]:
                                    todos_tem_epsilon = False
                                    break
                        
                        # Adicionar FIRST(resto) - {ε} a FOLLOW(simbolo)
                        antes = len(follow[simbolo])
                        follow[simbolo] |= first_resto
                        if len(follow[simbolo]) > antes:
                            mudou = True
                        
                        # Se todos têm epsilon, adicionar FOLLOW(nao_terminal)
                        if todos_tem_epsilon:
                            antes = len(follow[simbolo])
                            follow[simbolo] |= follow[nao_terminal]
                            if len(follow[simbolo]) > antes:
                                mudou = True
    
    return follow


# ============================================================================
# CONSTRUÇÃO DA TABELA LL(1)
# ============================================================================

def construirTabelaLL1(gramatica: Dict[str, List[List[str]]], 
                       first: Dict[str, Set[str]], 
                       follow: Dict[str, Set[str]]) -> Dict[str, Dict[str, int]]:
    """
    Constrói a tabela de análise LL(1).
    
    Para cada produção A → α:
    1. Para cada terminal a em FIRST(α), adiciona A → α a tabela[A][a]
    2. Se ε ∈ FIRST(α), para cada terminal b em FOLLOW(A), 
       adiciona A → α a tabela[A][b]
    
    Args:
        gramatica: Dicionário com as regras de produção
        first: Conjuntos FIRST
        follow: Conjuntos FOLLOW
        
    Returns:
        Tabela LL(1): tabela[não_terminal][terminal] = índice da produção
    """
    tabela = {}
    terminais = obter_terminais()
    
    for nao_terminal, producoes in gramatica.items():
        tabela[nao_terminal] = {}
        
        for idx_producao, producao in enumerate(producoes):
            # Calcular FIRST da produção
            if producao[0] == 'EPSILON':
                first_producao = {'EPSILON'}
            elif producao[0] in terminais:
                first_producao = {producao[0]}
            else:
                first_producao = first[producao[0]].copy()
                
                # Se primeiro símbolo pode derivar ε, continuar
                if 'EPSILON' in first_producao:
                    for simbolo in producao[1:]:
                        if simbolo in terminais:
                            first_producao.add(simbolo)
                            first_producao.discard('EPSILON')
                            break
                        else:
                            first_producao |= (first[simbolo] - {'EPSILON'})
                            if 'EPSILON' not in first[simbolo]:
                                first_producao.discard('EPSILON')
                                break
            
            # Para cada terminal em FIRST(produção)
            for terminal in first_producao:
                if terminal == 'EPSILON':
                    continue
                
                if terminal in tabela[nao_terminal]:
                    # CONFLITO DETECTADO
                    print(f"⚠️  CONFLITO em tabela[{nao_terminal}][{terminal}]")
                    print(f"   Produção {tabela[nao_terminal][terminal]} vs {idx_producao}")
                else:
                    tabela[nao_terminal][terminal] = idx_producao
            
            # Se ε está em FIRST(produção), usar FOLLOW
            if 'EPSILON' in first_producao:
                for terminal in follow[nao_terminal]:
                    if terminal in tabela[nao_terminal]:
                        # CONFLITO DETECTADO
                        print(f"⚠️  CONFLITO em tabela[{nao_terminal}][{terminal}]")
                        print(f"   Produção {tabela[nao_terminal][terminal]} vs {idx_producao}")
                    else:
                        tabela[nao_terminal][terminal] = idx_producao
    
    return tabela


# ============================================================================
# FUNÇÃO PRINCIPAL: construirGramatica()
# ============================================================================

def construirGramatica() -> Tuple[Dict, Dict, Dict, Dict]:
    """
    ALUNO 1: Função principal para construção da gramática LL(1).
    
    Esta função:
    1. Define as regras de produção da gramática com símbolos literais
    2. Calcula os conjuntos FIRST para todos os símbolos
    3. Calcula os conjuntos FOLLOW para todos os não-terminais
    4. Constrói a tabela de análise LL(1)
    
    Returns:
        Tupla contendo:
        - gramatica: Dict com as regras de produção (45 regras)
        - first: Dict com conjuntos FIRST
        - follow: Dict com conjuntos FOLLOW
        - tabela_ll1: Tabela de parsing LL(1)
    """
    print("Construindo gramática LL(1)...")
    
    # 1. Definir gramática
    gramatica = definir_gramatica()
    print(f"  ✓ Gramática definida: {len(gramatica)} não-terminais")
    
    # 2. Calcular FIRST
    first = calcularFirst(gramatica)
    print(f"  ✓ Conjuntos FIRST calculados")
    
    # 3. Calcular FOLLOW
    follow = calcularFollow(gramatica, first)
    print(f"  ✓ Conjuntos FOLLOW calculados")
    
    # 4. Construir tabela LL(1)
    tabela_ll1 = construirTabelaLL1(gramatica, first, follow)
    entradas = sum(len(t) for t in tabela_ll1.values())
    print(f"  ✓ Tabela LL(1) construída com {entradas} entradas")
    
    print("Gramática pronta!\n")
    
    return gramatica, first, follow, tabela_ll1


# ============================================================================
# TESTE BÁSICO (OPCIONAL)
# ============================================================================

if __name__ == "__main__":
    # Apenas construir e exibir estatísticas básicas
    gramatica, first, follow, tabela = construirGramatica()
    
    print("Estatísticas:")
    print(f"  - {len(gramatica)} não-terminais")
    print(f"  - {sum(len(prods) for prods in gramatica.values())} regras de produção")
    print(f"  - {len(obter_terminais())} terminais")
    print(f"  - {sum(len(t) for t in tabela.values())} entradas na tabela LL(1)")

# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

"""
construirGramatica.py - ALUNO 1
================================
Implementa a gramática LL(1) para RPN com todas as funções auxiliares.
"""

from typing import Dict, Set, List, Tuple

# ============================================================================
# DEFINIÇÃO DA GRAMÁTICA
# ============================================================================

def definir_gramatica() -> Dict[str, List[List[str]]]:
    """Define as 45 regras de produção da gramática RPN"""
    gramatica = {
        'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
        'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['EPSILON']],
        'LINHA': [['(', 'CONTENT', ')']],
        'CONTENT': [
            ['NUMBER', 'AFTER_NUM'],
            ['IDENTIFIER', 'AFTER_ID'],
            ['(', 'EXPR', ')', 'AFTER_EXPR'],
            ['FOR', 'FOR_STRUCT'],
            ['WHILE', 'WHILE_STRUCT'],
            ['IF', 'IF_STRUCT']
        ],
        'AFTER_NUM': [
            ['NUMBER', 'OPERATOR'],
            ['IDENTIFIER', 'MEM'],
            ['RES']
        ],
        'AFTER_ID': [
            ['NUMBER', 'OPERATOR'],
            ['IDENTIFIER', 'OPERATOR'],
            ['(', 'EXPR', ')', 'OPERATOR'],
            ['EPSILON']
        ],
        'AFTER_EXPR': [
            ['NUMBER', 'OPERATOR'],
            ['IDENTIFIER', 'OPERATOR'],
            ['(', 'EXPR', ')', 'OPERATOR']
        ],
        'EXPR': [
            ['NUMBER', 'AFTER_NUM'],
            ['IDENTIFIER', 'AFTER_ID'],
            ['(', 'EXPR', ')', 'AFTER_EXPR']
        ],
        'OPERATOR': [['ARITH_OP'], ['REL_OP'], ['LOGIC_OP']],
        'ARITH_OP': [['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^']],
        'REL_OP': [['>'], ['<'], ['=='], ['!='], ['>='], ['<=']],
        'LOGIC_OP': [['&&'], ['||'], ['!']],
        'FOR_STRUCT': [['NUMBER', 'NUMBER', 'IDENTIFIER', 'LINHA']],
        'WHILE_STRUCT': [['(', 'EXPR', ')', 'LINHA']],
        'IF_STRUCT': [['(', 'EXPR', ')', 'LINHA', 'ELSE', 'LINHA']]
    }
    return gramatica

def obter_terminais() -> Set[str]:
    """Retorna conjunto de símbolos terminais"""
    return {
        '(', ')', 'NUMBER', 'IDENTIFIER',
        '+', '-', '*', '|', '/', '%', '^',
        '>', '<', '==', '!=', '>=', '<=',
        '&&', '||', '!',
        'MEM', 'RES', 'FOR', 'WHILE', 'IF', 'ELSE',
        'EPSILON', 'EOF'
    }

def obter_nao_terminais(gramatica: Dict) -> Set[str]:
    """Retorna conjunto de não-terminais"""
    return set(gramatica.keys())

# ============================================================================
# CÁLCULO DOS CONJUNTOS FIRST
# ============================================================================

def calcularFirst(gramatica: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
    """Calcula conjuntos FIRST para cada não-terminal"""
    terminais = obter_terminais()
    nao_terminais = obter_nao_terminais(gramatica)
    
    first = {nt: set() for nt in nao_terminais}
    for terminal in terminais:
        first[terminal] = {terminal}
    
    mudou = True
    while mudou:
        mudou = False
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                if producao[0] == 'EPSILON':
                    if 'EPSILON' not in first[nao_terminal]:
                        first[nao_terminal].add('EPSILON')
                        mudou = True
                    continue
                
                for i, simbolo in enumerate(producao):
                    if simbolo in terminais:
                        simbolo_first = {simbolo}
                    else:
                        simbolo_first = first[simbolo].copy()
                    
                    antes = len(first[nao_terminal])
                    first[nao_terminal] |= (simbolo_first - {'EPSILON'})
                    if len(first[nao_terminal]) > antes:
                        mudou = True
                    
                    if 'EPSILON' not in simbolo_first:
                        break
                    
                    if i == len(producao) - 1:
                        if 'EPSILON' not in first[nao_terminal]:
                            first[nao_terminal].add('EPSILON')
                            mudou = True
    
    return first

# ============================================================================
# CÁLCULO DOS CONJUNTOS FOLLOW
# ============================================================================

def calcularFollow(gramatica: Dict[str, List[List[str]]], 
                   first: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Calcula conjuntos FOLLOW para cada não-terminal"""
    nao_terminais = obter_nao_terminais(gramatica)
    terminais = obter_terminais()
    
    follow = {nt: set() for nt in nao_terminais}
    follow['PROGRAM'].add('EOF')
    
    mudou = True
    while mudou:
        mudou = False
        for nao_terminal, producoes in gramatica.items():
            for producao in producoes:
                if producao[0] == 'EPSILON':
                    continue
                
                for i, simbolo in enumerate(producao):
                    if simbolo not in nao_terminais:
                        continue
                    
                    resto = producao[i + 1:]
                    
                    if not resto:
                        antes = len(follow[simbolo])
                        follow[simbolo] |= follow[nao_terminal]
                        if len(follow[simbolo]) > antes:
                            mudou = True
                    else:
                        first_resto = set()
                        todos_tem_epsilon = True
                        
                        for prox_simbolo in resto:
                            if prox_simbolo in terminais:
                                first_resto.add(prox_simbolo)
                                todos_tem_epsilon = False
                                break
                            else:
                                first_resto |= (first[prox_simbolo] - {'EPSILON'})
                                if 'EPSILON' not in first[prox_simbolo]:
                                    todos_tem_epsilon = False
                                    break
                        
                        antes = len(follow[simbolo])
                        follow[simbolo] |= first_resto
                        if len(follow[simbolo]) > antes:
                            mudou = True
                        
                        if todos_tem_epsilon:
                            antes = len(follow[simbolo])
                            follow[simbolo] |= follow[nao_terminal]
                            if len(follow[simbolo]) > antes:
                                mudou = True
    
    return follow

# ============================================================================
# CONSTRUÇÃO DA TABELA LL(1)
# ============================================================================

def construirTabelaLL1(gramatica: Dict[str, List[List[str]]], 
                       first: Dict[str, Set[str]], 
                       follow: Dict[str, Set[str]]) -> Dict[str, Dict[str, int]]:
    """Constrói tabela de análise LL(1)"""
    tabela = {}
    terminais = obter_terminais()
    
    for nao_terminal, producoes in gramatica.items():
        tabela[nao_terminal] = {}
        
        for idx_producao, producao in enumerate(producoes):
            if producao[0] == 'EPSILON':
                first_producao = {'EPSILON'}
            elif producao[0] in terminais:
                first_producao = {producao[0]}
            else:
                first_producao = first[producao[0]].copy()
                
                if 'EPSILON' in first_producao:
                    for simbolo in producao[1:]:
                        if simbolo in terminais:
                            first_producao.add(simbolo)
                            first_producao.discard('EPSILON')
                            break
                        else:
                            first_producao |= (first[simbolo] - {'EPSILON'})
                            if 'EPSILON' not in first[simbolo]:
                                first_producao.discard('EPSILON')
                                break
            
            for terminal in first_producao:
                if terminal == 'EPSILON':
                    continue
                if terminal in tabela[nao_terminal]:
                    print(f"CONFLITO em tabela[{nao_terminal}][{terminal}]")
                else:
                    tabela[nao_terminal][terminal] = idx_producao
            
            if 'EPSILON' in first_producao:
                for terminal in follow[nao_terminal]:
                    if terminal in tabela[nao_terminal]:
                        print(f"CONFLITO em tabela[{nao_terminal}][{terminal}]")
                    else:
                        tabela[nao_terminal][terminal] = idx_producao
    
    return tabela

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def construirGramatica() -> Tuple[Dict, Dict, Dict, Dict]:
    """
    Função principal que constrói a gramática LL(1) completa.
    
    Returns:
        Tupla (gramatica, first, follow, tabela_ll1)
    """
    print("Construindo gramática LL(1)...")
    
    gramatica = definir_gramatica()
    print(f"  Gramática definida: {len(gramatica)} não-terminais")
    
    first = calcularFirst(gramatica)
    print(f"  Conjuntos FIRST calculados")
    
    follow = calcularFollow(gramatica, first)
    print(f"  Conjuntos FOLLOW calculados")
    
    tabela_ll1 = construirTabelaLL1(gramatica, first, follow)
    print(f"  Tabela LL(1) construída")
    
    print("Gramática pronta!\n")
    
    return gramatica, first, follow, tabela_ll1

# ============================================================================
# TESTE
# ============================================================================

if __name__ == "__main__":
    gramatica, first, follow, tabela = construirGramatica()
    
    print("\nExemplo de entradas na tabela:")
    print(f"CONTENT tem {len(tabela['CONTENT'])} entradas")
    print(f"AFTER_NUM tem {len(tabela['AFTER_NUM'])} entradas")