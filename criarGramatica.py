# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

# ==================== CONSTRUIR GRAMÁTICA ====================

def construirGramatica():
    """
    Constrói a gramática LL(1) completa para a linguagem RPN.
    Responsabilidade do Aluno 1.
    
    Gramática corrigida sem ASSIGN e com MEM nas suas várias formas:
    - (V IDENTIFIER MEM) - armazenar valor em variável
    - (IDENTIFIER) - recuperar valor de variável  
    - (N RES) - resultado N linhas anteriores
    """
    productions = {
        'PROGRAM': [['STATEMENT_LIST']],
        'STATEMENT_LIST': [['STATEMENT', 'STATEMENT_LIST'], ['ε']],
        
        # Tipos de declarações - cada uma com FIRST disjunto
        'STATEMENT': [
            ['PAREN_STATEMENT'],  # Começa com '('
            ['ATOM'],             # Começa com NUMBER ou IDENTIFIER
            ['FOR_STATEMENT'],    # Começa com 'FOR'
            ['WHILE_STATEMENT'],  # Começa com 'WHILE'
            ['IF_STATEMENT']      # Começa com 'IF'
        ],
        
        # Declarações entre parênteses (várias formas)
        'PAREN_STATEMENT': [
            ['(', 'PAREN_CONTENT', ')']
        ],
        
        # Conteúdo dentro de parênteses - resolvendo conflito FIRST/FIRST
        'PAREN_CONTENT': [
            ['OPERAND', 'CONTENT_TAIL']  # Começa com operando, depois decide
        ],
        
        # Após primeiro operando, pode ser:
        'CONTENT_TAIL': [
            ['OPERAND', 'OPERATOR'],      # (A B +) - operação RPN
            ['IDENTIFIER', 'MEM'],        # (42 X MEM) - armazenar
            ['RES']                       # (3 RES) - resultado anterior
        ],
        
        # Átomos (fora de parênteses)
        'ATOM': [
            ['NUMBER'],
            ['IDENTIFIER']  # Variável sozinha recupera valor
        ],
        
        # Operandos (dentro de expressões)
        'OPERAND': [
            ['NUMBER'],
            ['IDENTIFIER'],
            ['PAREN_STATEMENT']  # Expressões aninhadas
        ],
        
        # Operadores aritméticos e relacionais
        'OPERATOR': [
            ['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^'],
            ['>'], ['<'], ['>='], ['<='], ['=='], ['!=']
        ],
        
        # Estruturas de controle
        'FOR_STATEMENT': [['FOR', '(', 'OPERAND', 'OPERAND', 'IDENTIFIER', 'STATEMENT', ')']],
        'WHILE_STATEMENT': [['WHILE', '(', 'PAREN_STATEMENT', 'STATEMENT', ')']],
        'IF_STATEMENT': [['IF', '(', 'PAREN_STATEMENT', 'STATEMENT', ')', 'IF_TAIL']],
        'IF_TAIL': [['ELSE', '(', 'STATEMENT', ')'], ['ε']]
    }
    
    nullable_set = calcularNullable(productions)
    first_sets = calcularFirst(productions, nullable_set)
    follow_sets = calcularFollow(productions, first_sets, nullable_set, 'PROGRAM')
    ll1_table = construirTabelaLL1(productions, first_sets, follow_sets)
    
    conflicts = detectarConflitos(productions, first_sets, follow_sets)
    if conflicts:
        raise ValueError(f"Gramática não é LL(1): {conflicts}")
    
    print("✓ Gramática validada como LL(1)")
    
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
    nullable = set()
    changed = True
    
    while changed:
        changed = False
        for lhs, rules in productions.items():
            if lhs not in nullable:
                for rule in rules:
                    if rule == ['ε'] or all(symbol in nullable for symbol in rule if symbol in productions):
                        nullable.add(lhs)
                        changed = True
                        break
    return nullable


def calcularFirst(productions, nullable):
    first_sets = {}
    terminais = extrairTerminais(productions)
    
    for terminal in terminais:
        first_sets[terminal] = {terminal}
    
    for non_terminal in productions.keys():
        first_sets[non_terminal] = set()
    
    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            old_size = len(first_sets[lhs])
            
            for rule in rules:
                if rule == ['ε']:
                    first_sets[lhs].add('ε')
                else:
                    for symbol in rule:
                        if symbol in terminais:
                            first_sets[lhs].add(symbol)
                            break
                        else:
                            first_sets[lhs].update(first_sets[symbol] - {'ε'})
                            if symbol not in nullable:
                                break
                    else:
                        first_sets[lhs].add('ε')
            
            if len(first_sets[lhs]) > old_size:
                changed = True
    
    return first_sets


def calcularFollow(productions, first_sets, nullable, start_symbol):
    follow_sets = {}
    
    for non_terminal in productions.keys():
        follow_sets[non_terminal] = set()
    
    follow_sets[start_symbol].add('$')
    
    changed = True
    while changed:
        changed = False
        
        for lhs, rules in productions.items():
            for rule in rules:
                for i, symbol in enumerate(rule):
                    if symbol in productions:
                        beta = rule[i + 1:]
                        old_size = len(follow_sets[symbol])
                        
                        if not beta:
                            follow_sets[symbol].update(follow_sets[lhs])
                        else:
                            first_beta = calcularFirstString(beta, first_sets, nullable)
                            follow_sets[symbol].update(first_beta - {'ε'})
                            
                            if 'ε' in first_beta:
                                follow_sets[symbol].update(follow_sets[lhs])
                        
                        if len(follow_sets[symbol]) > old_size:
                            changed = True
    
    return follow_sets


def calcularFirstString(symbols, first_sets, nullable):
    if not symbols:
        return {'ε'}
    
    result = set()
    for symbol in symbols:
        if symbol not in first_sets:
            result.add(symbol)
            break
        else:
            result.update(first_sets[symbol] - {'ε'})
            if symbol not in nullable:
                break
    else:
        result.add('ε')
    
    return result


def construirTabelaLL1(productions, first_sets, follow_sets):
    table = {}
    terminais = extrairTerminais(productions)
    terminais.add('$')
    
    for nt in productions.keys():
        table[nt] = {}
        for t in terminais:
            table[nt][t] = None
    
    for lhs, rules in productions.items():
        for rule in rules:
            production_name = f"{lhs} → {' '.join(rule)}"
            first_alpha = calcularFirstString(rule, first_sets, set() if rule != ['ε'] else {lhs})
            
            for terminal in first_alpha - {'ε'}:
                if table[lhs][terminal] is not None:
                    raise ValueError(f"Conflito FIRST/FIRST em [{lhs}, {terminal}]")
                table[lhs][terminal] = production_name
            
            if 'ε' in first_alpha:
                for terminal in follow_sets[lhs]:
                    if table[lhs][terminal] is not None:
                        raise ValueError(f"Conflito FIRST/FOLLOW em [{lhs}, {terminal}]")
                    table[lhs][terminal] = production_name
    
    return table


def detectarConflitos(productions, first_sets, follow_sets):
    conflicts = []
    
    for lhs, rules in productions.items():
        if len(rules) > 1:
            first_sets_rules = []
            for rule in rules:
                first_alpha = calcularFirstString(rule, first_sets, set() if rule != ['ε'] else {lhs})
                first_sets_rules.append(first_alpha)
            
            for i in range(len(first_sets_rules)):
                for j in range(i + 1, len(first_sets_rules)):
                    overlap = (first_sets_rules[i] - {'ε'}) & (first_sets_rules[j] - {'ε'})
                    if overlap:
                        conflicts.append(f"Conflito FIRST/FIRST em {lhs}: {overlap}")
            
            for i, first_set in enumerate(first_sets_rules):
                if 'ε' in first_set:
                    overlap = (first_set - {'ε'}) & follow_sets[lhs]
                    if overlap:
                        conflicts.append(f"Conflito FIRST/FOLLOW em {lhs}: {overlap}")
    
    return conflicts


def extrairTerminais(productions):
    terminais = set()
    non_terminais = set(productions.keys())
    
    for rules in productions.values():
        for rule in rules:
            for symbol in rule:
                if symbol not in non_terminais and symbol != 'ε':
                    terminais.add(symbol)
    
    return terminais


# ==================== PARSER LL(1) ====================

def parsear(tokens, tabela_ll1):
    """
    Parser LL(1) descendente recursivo.
    Responsabilidade do Aluno 2.
    """
    parsing_table = tabela_ll1['parsing_table']
    start_symbol = tabela_ll1['start_symbol']
    non_terminals = tabela_ll1['non_terminals']
    
    input_buffer = tokens + ['$']
    stack = ['$', start_symbol]
    position = 0
    derivation = []
    
    print(f"\n--- Iniciando parsing ---")
    print(f"Tokens: {tokens}")
    
    while len(stack) > 1:
        top = stack[-1]
        current_token = input_buffer[position] if position < len(input_buffer) else '$'
        
        if top not in non_terminals:
            if top == current_token:
                stack.pop()
                position += 1
                derivation.append(f"MATCH: {top}")
            else:
                return {
                    'success': False,
                    'error': f"Erro na posição {position}: esperado '{top}', encontrado '{current_token}'",
                    'position': position,
                    'derivation': derivation
                }
        else:
            if top in parsing_table and current_token in parsing_table[top]:
                production = parsing_table[top][current_token]
                
                if production is None:
                    return {
                        'success': False,
                        'error': f"Erro na posição {position}: sem regra para ({top}, {current_token})",
                        'position': position,
                        'derivation': derivation
                    }
                
                stack.pop()
                derivation.append(production)
                
                rhs = extrairLadoDireito(production)
                for symbol in reversed(rhs):
                    if symbol != 'ε':
                        stack.append(symbol)
            else:
                return {
                    'success': False,
                    'error': f"Erro na posição {position}: entrada inesperada '{current_token}' para '{top}'",
                    'position': position,
                    'derivation': derivation
                }
    
    if position == len(input_buffer) - 1:
        return {
            'success': True,
            'message': 'Parsing concluído com sucesso',
            'derivation': derivation,
            'tokens_processed': len(tokens)
        }
    else:
        return {
            'success': False,
            'error': f"Entrada não totalmente consumida",
            'position': position,
            'derivation': derivation
        }


def extrairLadoDireito(production):
    if '→' in production:
        rhs = production.split('→')[1].strip()
    else:
        rhs = production.split('->')[1].strip()
    return rhs.split()


# ==================== TESTES ====================

def testar():
    print("="*60)
    print("TESTANDO ANALISADOR SINTÁTICO LL(1) - FASE 2")
    print("="*60)
    
    # 1. Construir gramática
    print("\n1. Construindo gramática...")
    try:
        tabela_ll1 = construirGramatica()
        print(f"   Não-terminais: {len(tabela_ll1['non_terminals'])}")
        print(f"   Terminais: {len(tabela_ll1['terminals'])}")
    except Exception as e:
        print(f"   ERRO: {e}")
        return
    
    # 2. Casos de teste
    test_cases = [
        {
            'name': 'Expressão RPN simples',
            'tokens': ['(', 'NUMBER', 'NUMBER', '+', ')'],
            'expected': True
        },
        {
            'name': 'Armazenar em memória',
            'tokens': ['(', 'NUMBER', 'IDENTIFIER', 'MEM', ')'],
            'expected': True
        },
        {
            'name': 'Recuperar de memória',
            'tokens': ['(', 'IDENTIFIER', ')'],
            'expected': True
        },
        {
            'name': 'Usar RES',
            'tokens': ['(', 'NUMBER', 'RES', ')'],
            'expected': True
        },
        {
            'name': 'Expressão aninhada',
            'tokens': ['(', '(', 'NUMBER', 'NUMBER', '*', ')', 'NUMBER', '+', ')'],
            'expected': True
        },
        {
            'name': 'FOR Loop',
            'tokens': ['FOR', '(', 'NUMBER', 'NUMBER', 'IDENTIFIER', 'NUMBER', ')'],
            'expected': True
        },
        {
            'name': 'Átomo simples',
            'tokens': ['NUMBER'],
            'expected': True
        },
        {
            'name': 'ERRO - Parênteses',
            'tokens': ['(', 'NUMBER', 'NUMBER', '+'],
            'expected': False
        }
    ]
    
    # 3. Executar testes
    print("\n2. Executando testes...\n")
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTeste {i}: {test['name']}")
        print(f"Tokens: {test['tokens']}")
        
        resultado = parsear(test['tokens'], tabela_ll1)
        
        if resultado['success'] == test['expected']:
            print(f"✓ PASSOU")
            passed += 1
        else:
            print(f"✗ FALHOU")
            failed += 1
        
        if resultado['success']:
            print(f"  Processados: {resultado['tokens_processed']} tokens")
        else:
            print(f"  Erro: {resultado['error']}")
    
    # 4. Resumo
    print("\n" + "="*60)
    print(f"RESUMO: {passed} passou | {failed} falhou")
    print("="*60)


if __name__ == "__main__":
    testar()