# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

"""
GRAMÁTICA LL(1) PARA CALCULADORA RPN COM ESTRUTURAS DE CONTROLE
================================================================
Baseada na gramática provadamente LL(1) dos documentos teóricos (arquivos 06 e 07)
"""

# ==================== UTILIDADES ====================

def extrairTerminais(productions):
    """Extrai todos os terminais da gramática"""
    terminais = set()
    non_terminais = set(productions.keys())
    for rules in productions.values():
        for rule in rules:
            for symbol in rule:
                if symbol not in non_terminais and symbol != 'ε':
                    terminais.add(symbol)
    return terminais

def calcularFirstString(symbols, first_sets, nullable):
    """Calcula FIRST de uma sequência de símbolos"""
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

# ==================== CÁLCULO DE CONJUNTOS ====================

def calcularNullable(productions):
    """Calcula conjunto NULLABLE - CORRIGIDO"""
    nullable = set()
    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            if lhs not in nullable:
                for rule in rules:
                    # Caso 1: produção epsilon direta
                    if rule == ['ε']:
                        nullable.add(lhs)
                        changed = True
                        break
                    # Caso 2: TODOS os símbolos devem ser não-terminais E nullable
                    # Se tiver qualquer terminal, NÃO é nullable
                    elif all(symbol in productions and symbol in nullable for symbol in rule):
                        nullable.add(lhs)
                        changed = True
                        break
    return nullable

def calcularFirst(productions, nullable):
    """Calcula conjuntos FIRST para todos os símbolos"""
    first_sets = {}
    terminais = extrairTerminais(productions)
    
    # Inicializar terminais
    for terminal in terminais:
        first_sets[terminal] = {terminal}
    
    # Inicializar não-terminais
    for non_terminal in productions.keys():
        first_sets[non_terminal] = set()
    
    # Iteração até ponto fixo
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
    """Calcula conjuntos FOLLOW para não-terminais"""
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

def construirTabelaLL1(productions, first_sets, follow_sets, nullable):
    """Constrói tabela LL(1)"""
    table = {}
    terminais = extrairTerminais(productions)
    terminais.add('$')
    
    # Inicializar tabela
    for nt in productions.keys():
        table[nt] = {}
        for t in terminais:
            table[nt][t] = None
    
    # Preencher tabela
    for lhs, rules in productions.items():
        for rule in rules:
            production_name = f"{lhs} → {' '.join(rule)}"
            first_alpha = calcularFirstString(rule, first_sets, nullable)
            
            # Regra FIRST
            for terminal in first_alpha - {'ε'}:
                if table[lhs][terminal] is not None:
                    raise ValueError(f"CONFLITO FIRST/FIRST em [{lhs}, {terminal}]")
                table[lhs][terminal] = production_name
            
            # Regra FOLLOW (para produções epsilon)
            if 'ε' in first_alpha:
                for terminal in follow_sets[lhs]:
                    if table[lhs][terminal] is not None:
                        raise ValueError(f"CONFLITO FIRST/FOLLOW em [{lhs}, {terminal}]")
                    table[lhs][terminal] = production_name
    return table

# ==================== GRAMÁTICA LL(1) SIMPLIFICADA ====================

def construirGramatica():
    """
    Gramática LL(1) baseada nos documentos teóricos
    
    SIMPLIFICADA conforme especificação:
    - Sem ASSIGN_STATEMENT (não necessário)
    - MEM e RES como comandos especiais nas expressões RPN
    """
    
    productions = {
        # Estrutura básica do programa
        'PROGRAM': [['STATEMENT_LIST']],
        
        'STATEMENT_LIST': [
            ['STATEMENT', 'STATEMENT_LIST'],
            ['ε']
        ],
        
        'STATEMENT': [
            ['EXPRESSION'],
            ['ATOM'],                # Número/ID solto
            ['FOR_STATEMENT'],
            ['WHILE_STATEMENT'],
            ['IF_STATEMENT']
        ],
        
        # Expressão SEMPRE entre parênteses (elimina ambiguidade)
        'EXPRESSION': [
            ['(', 'EXPR_CONTENT', ')']
        ],
        
        # Conteúdo das expressões (diferentes padrões RPN)
        'EXPR_CONTENT': [
            ['OPERAND', 'OPERAND', 'OPERATOR'],  # Binário: (A B +)
            ['NUMBER', 'RES'],                   # Resultado anterior: (N RES)
            ['OPERAND', 'IDENTIFIER', 'MEM'],    # Armazenar: (V MEM)
            ['IDENTIFIER']                       # Recuperar memória: (VAR)
        ],
        
        # Operando pode ser átomo OU expressão (aninhamento)
        'OPERAND': [
            ['ATOM'],
            ['EXPRESSION']
        ],
        
        # Átomos básicos
        'ATOM': [
            ['NUMBER'],
            ['IDENTIFIER']
        ],
        
        'OPERATOR': [
            ['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^'],
            ['>'], ['<'], ['>='], ['<='], ['=='], ['!=']
        ],
        
        # Estruturas de controle
        'FOR_STATEMENT': [
            ['FOR', '(', 'OPERAND', 'OPERAND', 'IDENTIFIER', 'STATEMENT', ')']
        ],
        
        'WHILE_STATEMENT': [
            ['WHILE', '(', 'EXPRESSION', 'STATEMENT', ')']
        ],
        
        'IF_STATEMENT': [
            ['IF', '(', 'EXPRESSION', 'STATEMENT', ')', 'IF_TAIL']
        ],
        
        'IF_TAIL': [
            ['ELSE', '(', 'STATEMENT', ')'],
            ['ε']
        ]
    }
    
    print("="*70)
    print("CONSTRUINDO GRAMÁTICA LL(1)")
    print("="*70)
    
    print("\nCalculando NULLABLE...")
    nullable_set = calcularNullable(productions)
    print(f"NULLABLE = {nullable_set}")
    
    print("\nCalculando FIRST...")
    first_sets = calcularFirst(productions, nullable_set)
    
    print("\nCalculando FOLLOW...")
    follow_sets = calcularFollow(productions, first_sets, nullable_set, 'PROGRAM')
    
    print("\nConstruindo tabela LL(1)...")
    try:
        ll1_table = construirTabelaLL1(productions, first_sets, follow_sets, nullable_set)
        print("✓ Tabela LL(1) construída sem conflitos!")
    except ValueError as e:
        print(f"✗ ERRO: {e}")
        return None
    
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

# ==================== PARSER ====================

def extrairLadoDireito(production):
    """Extrai lado direito de uma produção"""
    if '→' in production:
        rhs = production.split('→')[1].strip()
    else:
        rhs = production.split('->')[1].strip()
    return rhs.split()

def parsear(tokens, tabela_ll1, verbose=False):
    """
    Parser LL(1) descendente recursivo com pilha
    """
    parsing_table = tabela_ll1['parsing_table']
    start_symbol = tabela_ll1['start_symbol']
    non_terminals = tabela_ll1['non_terminals']
    
    input_buffer = tokens + ['$']
    stack = ['$', start_symbol]
    position = 0
    derivation = []
    
    if verbose:
        print("\n" + "="*70)
        print("INICIANDO PARSING")
        print("="*70)
        print(f"Entrada: {' '.join(tokens)}")
        print()
    
    step = 0
    while len(stack) > 1:
        step += 1
        top = stack[-1]
        current_token = input_buffer[position] if position < len(input_buffer) else '$'
        
        if verbose:
            print(f"Passo {step}:")
            print(f"  Stack: {' '.join(stack)}")
            print(f"  Próximo token: {current_token}")
        
        if top not in non_terminals:  # Terminal
            if top == current_token:
                stack.pop()
                position += 1
                derivation.append(f"MATCH: {top}")
                if verbose:
                    print(f"  → Match: {top}")
            else:
                return {
                    'success': False,
                    'error': f"Erro na posição {position}: esperado '{top}', encontrado '{current_token}'",
                    'position': position,
                    'derivation': derivation
                }
        else:  # Não-terminal
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
                
                if verbose:
                    print(f"  → Aplicar: {production}")
                
                for symbol in reversed(rhs):
                    if symbol != 'ε':
                        stack.append(symbol)
            else:
                return {
                    'success': False,
                    'error': f"Erro na posição {position}: entrada inesperada '{current_token}'",
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
            'error': 'Entrada não totalmente consumida',
            'position': position,
            'derivation': derivation
        }

# ==================== TESTES ====================

def exibirConjuntos(tabela_ll1):
    """Exibe os conjuntos FIRST e FOLLOW calculados"""
    print("\n" + "="*70)
    print("CONJUNTOS FIRST")
    print("="*70)
    for symbol in sorted(tabela_ll1['first_sets'].keys()):
        first_set = tabela_ll1['first_sets'][symbol]
        print(f"FIRST({symbol:20s}) = {{{', '.join(sorted(first_set))}}}")
    
    print("\n" + "="*70)
    print("CONJUNTOS FOLLOW")
    print("="*70)
    for symbol in sorted(tabela_ll1['follow_sets'].keys()):
        follow_set = tabela_ll1['follow_sets'][symbol]
        print(f"FOLLOW({symbol:20s}) = {{{', '.join(sorted(follow_set))}}}")

def testar():
    """Executa bateria de testes"""
    print("\n" + "="*70)
    print("TESTANDO GRAMÁTICA LL(1) PARA RPN")
    print("="*70)
    
    tabela_ll1 = construirGramatica()
    if tabela_ll1 is None:
        print("\n✗ FALHA: Gramática contém conflitos")
        return
    
    # Exibir conjuntos
    exibirConjuntos(tabela_ll1)
    
    # Casos de teste
    print("\n" + "="*70)
    print("CASOS DE TESTE")
    print("="*70)
    
    test_cases = [
        # Expressões básicas
        (['(', '3', '4', '+', ')'], 'Expressão RPN simples: (3 4 +)'),
        (['(', 'X', 'Y', '*', ')'], 'Expressão com identificadores: (X Y *)'),
        (['42'], 'Operando único: 42'),
        (['VAR'], 'Identificador único: VAR'),
        
        # Expressões aninhadas
        (['(', '(', 'A', 'B', '+', ')', 'C', '*', ')'], 'Aninhada: ((A B +) C *)'),
        (['(', '(', '(', '1', '2', '+', ')', '3', '*', ')', '4', '/', ')'], 'Triplo aninhamento'),
        
        # Comandos especiais RPN
        (['(', '5', 'RESULT', 'MEM', ')'], 'Armazenar em memória: (5 RESULT MEM)'),
        (['(', '(', 'X', 'Y', '+', ')', 'TOTAL', 'MEM', ')'], 'Armazenar expressão: ((X Y +) TOTAL MEM)'),
        (['(', '2', 'RES', ')'], 'Usar resultado anterior: (2 RES)'),
        (['(', '0', 'RES', ')'], 'Resultado linha atual: (0 RES)'),
        
        # Estruturas de controle
        (['FOR', '(', '1', '10', 'I', '(', 'I', 'X', '+', ')', ')'], 'Loop FOR com expressão'),
        (['WHILE', '(', '(', 'X', '0', '>', ')', '(', 'X', 'Y', '-', ')', ')'], 'Loop WHILE'),
        (['IF', '(', '(', 'X', '5', '>', ')', '(', 'A', 'B', '*', ')', ')'], 'IF sem ELSE'),
        (['IF', '(', '(', 'A', 'B', '>', ')', 'YES', ')', 'ELSE', '(', 'NO', ')'], 'IF-ELSE'),
        
        # Programa com múltiplos statements
        (['(', '1', 'X', 'MEM', ')', '(', '2', 'Y', 'MEM', ')', '(', 'X', 'Y', '+', ')'], 
         'Programa: armazena X e Y, depois soma'),
        
        # Casos inválidos (devem falhar)
        (['(', '1', '2'], 'Inválido: parênteses não fechados'),
        ([')', '1', '2', '+', ')'], 'Inválido: parênteses desordenados'),
    ]
    
    passed = 0
    failed = 0
    
    for tokens, desc in test_cases:
        print(f"\n[TESTE] {desc}")
        print(f"Tokens: {' '.join(tokens)}")
        resultado = parsear(tokens, tabela_ll1, verbose=False)
        
        if resultado['success']:
            print(f"✓ ACEITO")
            passed += 1
        else:
            print(f"✗ REJEITADO: {resultado['error']}")
            failed += 1
    
    # Resumo
    print("\n" + "="*70)
    print(f"RESUMO: {passed} testes passaram, {failed} falharam")
    print("="*70)
    
    # Teste detalhado com verbose
    print("\n" + "="*70)
    print("EXEMPLO DE PARSING DETALHADO")
    print("="*70)
    tokens_exemplo = ['(', '(', 'A', 'B', '+', ')', 'C', '*', ')']
    resultado = parsear(tokens_exemplo, tabela_ll1, verbose=True)
    print(f"\nResultado: {'ACEITO' if resultado['success'] else 'REJEITADO'}")

if __name__ == "__main__":
    testar()