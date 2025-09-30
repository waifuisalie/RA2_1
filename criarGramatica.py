# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

def construirGramatica():
    """
    Constrói a gramática LL(1) completa para a linguagem RPN com estruturas de controle.
    
    Esta função implementa a responsabilidade do Aluno 1 conforme especificação do PDF:
    - Define as regras de produção da linguagem
    - Calcula os conjuntos FIRST e FOLLOW
    - Constrói a tabela de análise LL(1)
    - Valida que a gramática é LL(1) (sem conflitos)
    
    Returns:
        dict: Estrutura completa contendo gramática, conjuntos FIRST/FOLLOW e tabela LL(1)
    """
    
    # 1. Definir as regras de produção da linguagem RPN
    productions = {
        # Estrutura do programa
        'PROGRAM': [['STATEMENT_LIST']],
        'STATEMENT_LIST': [['STATEMENT', 'STATEMENT_LIST'], ['ε']],
        
        # Tipos de declarações (cada uma com FIRST disjunto)
        'STATEMENT': [
            ['PAREN_EXPR'],      # Começa com '('
            ['ATOM'],            # Começa com NUMBER ou IDENTIFIER
            ['FOR_STATEMENT'],   # Começa com 'FOR'
            ['WHILE_STATEMENT'], # Começa com 'WHILE'
            ['IF_STATEMENT'],    # Começa com 'IF'
            ['ASSIGN_STATEMENT'],# Começa com 'ASSIGN'
            ['MEM_REF']          # Começa com 'MEM'
        ],
        
        # Expressão entre parênteses (RPN)
        'PAREN_EXPR': [
            ['(', 'OPERAND', 'OPERAND', 'OPERATOR', ')']
        ],
        
        # Átomos (literais simples)
        'ATOM': [
            ['NUMBER'],
            ['IDENTIFIER']
        ],
        
        # Referência de memória
        'MEM_REF': [
            ['MEM', '(', 'IDENTIFIER', ')']
        ],
        
        # Operandos (usado dentro de expressões)
        'OPERAND': [
            ['NUMBER'],
            ['IDENTIFIER'],
            ['PAREN_EXPR'],
            ['MEM_REF']
        ],
        
        # Operadores aritméticos e relacionais
        'OPERATOR': [
            ['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^'],  # Aritméticos
            ['>'], ['<'], ['>='], ['<='], ['=='], ['!=']      # Relacionais
        ],
        
        # Estruturas de controle em notação pós-fixada
        'FOR_STATEMENT': [['FOR', '(', 'OPERAND', 'OPERAND', 'IDENTIFIER', 'STATEMENT', ')']],
        'WHILE_STATEMENT': [['WHILE', '(', 'PAREN_EXPR', 'STATEMENT', ')']],
        'IF_STATEMENT': [['IF', '(', 'PAREN_EXPR', 'STATEMENT', ')', 'IF_TAIL']],
        'IF_TAIL': [['ELSE', '(', 'STATEMENT', ')'], ['ε']],
        'ASSIGN_STATEMENT': [['ASSIGN', '(', 'OPERAND', 'IDENTIFIER', ')']]
    }
    
    # 2. Calcular conjuntos FIRST e FOLLOW
    nullable_set = calcularNullable(productions)
    first_sets = calcularFirst(productions, nullable_set)
    follow_sets = calcularFollow(productions, first_sets, nullable_set, 'PROGRAM')
    
    # 3. Construir tabela LL(1)
    ll1_table = construirTabelaLL1(productions, first_sets, follow_sets)
    
    # 4. Validar gramática LL(1)
    conflicts = detectarConflitos(productions, first_sets, follow_sets)
    if conflicts:
        raise ValueError(f"Gramática não é LL(1). Conflitos detectados: {conflicts}")
    
    print("✅ Gramática validada como LL(1) - sem conflitos detectados")
    
    # 5. Retornar estrutura completa para integração
    return {
        'productions': productions,
        'nullable': nullable_set,
        'first_sets': first_sets,
        'follow_sets': follow_sets,
        'parsing_table': ll1_table,
        'start_symbol': 'PROGRAM',
        'terminals': extrairTerminais(productions),
        'non_terminals': set(productions.keys())
    }


def calcularNullable(productions):
    """
    Calcula o conjunto NULLABLE usando algoritmo iterativo.
    
    NULLABLE(A) = True se A pode derivar a string vazia (ε)
    """
    nullable = set()
    changed = True
    
    while changed:
        changed = False
        for lhs, rules in productions.items():
            if lhs not in nullable:
                for rule in rules:
                    # Produção direta para ε ou todos os símbolos são nullable
                    if rule == ['ε'] or all(symbol in nullable for symbol in rule if symbol in productions):
                        nullable.add(lhs)
                        changed = True
                        break
    
    return nullable


def calcularFirst(productions, nullable):
    """
    Calcula conjuntos FIRST usando algoritmo iterativo.
    
    FIRST(A) = conjunto de terminais que podem iniciar strings derivadas de A
    """
    first_sets = {}
    
    # Inicializar terminais
    terminais = extrairTerminais(productions)
    for terminal in terminais:
        first_sets[terminal] = {terminal}
    
    # Inicializar não-terminais
    for non_terminal in productions.keys():
        first_sets[non_terminal] = set()
    
    # Algoritmo iterativo
    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            old_size = len(first_sets[lhs])
            
            for rule in rules:
                if rule == ['ε']:
                    first_sets[lhs].add('ε')
                else:
                    # Adicionar FIRST de cada símbolo até encontrar não-nullable
                    for symbol in rule:
                        if symbol in terminais:
                            first_sets[lhs].add(symbol)
                            break
                        else:
                            first_sets[lhs].update(first_sets[symbol] - {'ε'})
                            if symbol not in nullable:
                                break
                    else:
                        # Todos os símbolos eram nullable
                        first_sets[lhs].add('ε')
            
            if len(first_sets[lhs]) > old_size:
                changed = True
    
    return first_sets


def calcularFollow(productions, first_sets, nullable, start_symbol):
    """
    Calcula conjuntos FOLLOW usando algoritmo iterativo.
    
    FOLLOW(A) = conjunto de terminais que podem aparecer imediatamente após A
    """
    follow_sets = {}
    
    # Inicializar não-terminais
    for non_terminal in productions.keys():
        follow_sets[non_terminal] = set()
    
    # Regra 1: Adicionar $ ao símbolo inicial
    follow_sets[start_symbol].add('$')
    
    # Algoritmo iterativo
    changed = True
    while changed:
        changed = False
        
        for lhs, rules in productions.items():
            for rule in rules:
                for i, symbol in enumerate(rule):
                    if symbol in productions:  # É não-terminal
                        beta = rule[i + 1:]  # Símbolos após o símbolo atual
                        old_size = len(follow_sets[symbol])
                        
                        if not beta:  # A → αB (B no final)
                            follow_sets[symbol].update(follow_sets[lhs])
                        else:  # A → αBβ (B no meio)
                            first_beta = calcularFirstString(beta, first_sets, nullable)
                            follow_sets[symbol].update(first_beta - {'ε'})
                            
                            if 'ε' in first_beta:
                                follow_sets[symbol].update(follow_sets[lhs])
                        
                        if len(follow_sets[symbol]) > old_size:
                            changed = True
    
    return follow_sets


def calcularFirstString(symbols, first_sets, nullable):
    """
    Calcula FIRST de uma sequência de símbolos.
    """
    if not symbols:
        return {'ε'}
    
    result = set()
    for symbol in symbols:
        if symbol not in first_sets:
            result.add(symbol)  # Terminal
            break
        else:
            result.update(first_sets[symbol] - {'ε'})
            if symbol not in nullable:
                break
    else:
        # Todos os símbolos eram nullable
        result.add('ε')
    
    return result


def construirTabelaLL1(productions, first_sets, follow_sets):
    """
    Constrói a tabela de análise LL(1).
    
    Tabela[A, a] = produção a usar quando vemos não-terminal A e terminal a
    """
    table = {}
    terminais = extrairTerminais(productions)
    terminais.add('$')
    
    # Inicializar tabela vazia
    for nt in productions.keys():
        table[nt] = {}
        for t in terminais:
            table[nt][t] = None
    
    # Preencher tabela usando regras FIRST e FOLLOW
    for lhs, rules in productions.items():
        for i, rule in enumerate(rules):
            production_name = f"{lhs} → {' '.join(rule)}"
            first_alpha = calcularFirstString(rule, first_sets, set() if rule != ['ε'] else {lhs})
            
            # Regra FIRST
            for terminal in first_alpha - {'ε'}:
                if table[lhs][terminal] is not None:
                    raise ValueError(f"Conflito FIRST/FIRST em [{lhs}, {terminal}]")
                table[lhs][terminal] = production_name
            
            # Regra FOLLOW 
            if 'ε' in first_alpha:
                for terminal in follow_sets[lhs]:
                    if table[lhs][terminal] is not None:
                        raise ValueError(f"Conflito FIRST/FOLLOW em [{lhs}, {terminal}]")
                    table[lhs][terminal] = production_name
    
    return table


def detectarConflitos(productions, first_sets, follow_sets):
    """
    Detecta conflitos LL(1) na gramática.
    """
    conflicts = []
    
    # Agrupar produções por não-terminal
    for lhs, rules in productions.items():
        if len(rules) > 1:  # Múltiplas alternativas
            first_sets_rules = []
            for rule in rules:
                first_alpha = calcularFirstString(rule, first_sets, set() if rule != ['ε'] else {lhs})
                first_sets_rules.append(first_alpha)
            
            # Verificar conflitos FIRST/FIRST
            for i in range(len(first_sets_rules)):
                for j in range(i + 1, len(first_sets_rules)):
                    overlap = (first_sets_rules[i] - {'ε'}) & (first_sets_rules[j] - {'ε'})
                    if overlap:
                        conflicts.append(f"Conflito FIRST/FIRST em {lhs}: {overlap}")
            
            # Verificar conflitos FIRST/FOLLOW
            for i, first_set in enumerate(first_sets_rules):
                if 'ε' in first_set:
                    overlap = (first_set - {'ε'}) & follow_sets[lhs]
                    if overlap:
                        conflicts.append(f"Conflito FIRST/FOLLOW em {lhs}: {overlap}")
    
    return conflicts


def extrairTerminais(productions):
    """
    Extrai todos os símbolos terminais das produções.
    """
    terminais = set()
    non_terminais = set(productions.keys())
    
    for rules in productions.values():
        for rule in rules:
            for symbol in rule:
                if symbol not in non_terminais and symbol != 'ε':
                    terminais.add(symbol)
    
    return terminais


# Função auxiliar para testes
def testarGramatica():
    """
    Testa a construção da gramática com casos de exemplo.
    """
    try:
        resultado = construirGramatica()
        
        print("\n=== RESULTADO DA CONSTRUÇÃO DA GRAMÁTICA ===")
        print(f"✅ Gramática construída com sucesso!")
        print(f"📊 Não-terminais: {len(resultado['non_terminals'])}")
        print(f"📊 Terminais: {len(resultado['terminals'])}")
        print(f"📊 Produções: {sum(len(rules) for rules in resultado['productions'].values())}")
        
        print("\n=== CONJUNTOS FIRST (primeiros 5) ===")
        for i, (nt, first_set) in enumerate(list(resultado['first_sets'].items())[:5]):
            print(f"FIRST({nt}) = {first_set}")
        
        print("\n=== CONJUNTOS FOLLOW (primeiros 5) ===") 
        for i, (nt, follow_set) in enumerate(list(resultado['follow_sets'].items())[:5]):
            print(f"FOLLOW({nt}) = {follow_set}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Erro na construção da gramática: {e}")
        return None


if __name__ == "__main__":
    testarGramatica()