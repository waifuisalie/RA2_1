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



def parsear(tokens, tabela_ll1):
    """
    Implementa o analisador sintático descendente recursivo LL(1).
    
    Esta função implementa a responsabilidade do Aluno 2 conforme especificação do PDF:
    - Usa a tabela LL(1) para guiar o processo de parsing
    - Implementa a pilha de análise e controle de derivação
    - Detecta e reporta erros sintáticos com mensagens claras
    - Gera a estrutura de derivação durante o parsing
    
    Args:
        tokens (list): Vetor de tokens gerado por lerTokens()
        tabela_ll1 (dict): Estrutura retornada por construirGramatica()
        
    Returns:
        dict: Resultado do parsing com derivação ou erro sintático
    """
    
    # Extrair componentes da tabela LL(1)
    parsing_table = tabela_ll1['parsing_table']
    start_symbol = tabela_ll1['start_symbol'] 
    non_terminals = tabela_ll1['non_terminals']
    
    # Inicializar estruturas de parsing
    input_buffer = tokens + ['$']  # Adicionar marcador de fim
    stack = ['$', start_symbol]    # Pilha com $ e símbolo inicial
    position = 0                   # Posição atual no buffer de entrada
    derivation = []               # Sequência de derivação para gerarArvore
    
    print(f"🔍 Iniciando parsing LL(1)")
    print(f"📝 Tokens de entrada: {tokens}")
    print(f"🎯 Símbolo inicial: {start_symbol}")
    
    # Algoritmo principal LL(1)
    while len(stack) > 1:  # Continue até só restar $ na pilha
        top = stack[-1]  # Topo da pilha
        current_token = input_buffer[position] if position < len(input_buffer) else '$'
        
        print(f"\n📊 Estado atual:")
        print(f"   Pilha: {stack}")
        print(f"   Token atual: {current_token} (pos {position})")
        
        # Caso 1: Topo da pilha é terminal
        if top not in non_terminals:
            if top == current_token:
                # Match bem-sucedido
                matched_symbol = stack.pop()
                position += 1
                derivation.append(f"MATCH: {matched_symbol}")
                print(f"✅ Match: {matched_symbol}")
            else:
                # Erro: terminal esperado não confere
                return criarErroSintatico(
                    f"Erro sintático na posição {position}: "
                    f"esperado '{top}', encontrado '{current_token}'",
                    position, current_token, derivation
                )
        
        # Caso 2: Topo da pilha é não-terminal
        else:
            # Buscar regra na tabela LL(1)
            if top in parsing_table and current_token in parsing_table[top]:
                production = parsing_table[top][current_token]
                
                if production is None:
                    # Entrada vazia na tabela = erro sintático
                    return criarErroSintatico(
                        f"Erro sintático na posição {position}: "
                        f"não há regra para ({top}, {current_token})",
                        position, current_token, derivation
                    )
                
                # Aplicar produção
                stack.pop()  # Remove não-terminal da pilha
                derivation.append(production)
                print(f"📋 Aplicando: {production}")
                
                # Extrair lado direito da produção
                rhs = extrairLadoDireito(production)
                
                # Empilhar símbolos em ordem reversa (exceto ε)
                for symbol in reversed(rhs):
                    if symbol != 'ε':
                        stack.append(symbol)
                        
                print(f"📚 Nova pilha: {stack}")
                
            else:
                # Não-terminal ou token não encontrado na tabela
                return criarErroSintatico(
                    f"Erro sintático na posição {position}: "
                    f"entrada inesperada '{current_token}' para não-terminal '{top}'",
                    position, current_token, derivation
                )
    
    # Verificar se entrada foi totalmente consumida
    if position == len(input_buffer) - 1:  # Apenas $ deve restar
        return {
            'success': True,
            'message': 'Parsing concluído com sucesso',
            'derivation': derivation,
            'tokens_processed': len(tokens)
        }
    else:
        return criarErroSintatico(
            f"Erro sintático: entrada não totalmente consumida. "
            f"Restam tokens: {input_buffer[position:]}",
            position, input_buffer[position] if position < len(input_buffer) else 'EOF',
            derivation
        )


def extrairLadoDireito(production):
    """
    Extrai o lado direito de uma produção no formato "A → α".
    
    Args:
        production (str): Produção no formato "LHS → RHS"
        
    Returns:
        list: Lista de símbolos do lado direito
    """
    if '→' in production:
        rhs = production.split('→')[1].strip()
    else:
        rhs = production.split('->')[1].strip()
    
    return rhs.split()


def criarErroSintatico(mensagem, posicao, token, derivacao):
    """
    Cria estrutura de erro sintático padronizada.
    """
    return {
        'success': False,
        'error': mensagem,
        'position': posicao,
        'unexpected_token': token,
        'derivation': derivacao,
        'recovery_suggestion': sugerirRecuperacao(token, posicao)
    }


def sugerirRecuperacao(token, posicao):
    """
    Sugere estratégias de recuperação de erro básicas.
    """
    suggestions = {
        '(': "Verifique se há ')' correspondente",
        ')': "Verifique se há '(' correspondente", 
        '+': "Verifique se há dois operandos antes do operador",
        'FOR': "Formato esperado: FOR ( inicio fim contador declaracao )",
        'IF': "Formato esperado: IF ( condicao declaracao )",
        'WHILE': "Formato esperado: WHILE ( condicao declaracao )",
    }
    
    return suggestions.get(token, f"Verifique a sintaxe próxima à posição {posicao}")


def validarEntrada(tokens, tabela_ll1):
    """
    Valida se a entrada está no formato correto antes do parsing.
    """
    if not tokens:
        return False, "Lista de tokens está vazia"
    
    if not tabela_ll1:
        return False, "Tabela LL(1) não foi fornecida"
    
    required_keys = ['parsing_table', 'start_symbol', 'non_terminals']
    for key in required_keys:
        if key not in tabela_ll1:
            return False, f"Chave '{key}' ausente na tabela LL(1)"
    
    return True, "Entrada válida"


def testarParser():
    """
    Testa o parser com casos de exemplo usando a gramática construída.
    """
    # Importar a função construirGramatica (assumindo que está no mesmo arquivo)
    try:
        from construir_gramatica import construirGramatica
        tabela_ll1 = construirGramatica()
    except:
        print("❌ Erro: função construirGramatica() não encontrada")
        return
    
    # Casos de teste
    test_cases = [
        # Expressão simples
        {
            'name': 'Expressão Simples',
            'tokens': ['(', '3', '4', '+', ')'],
            'expected': True
        },
        
        # FOR loop
        {
            'name': 'FOR Loop', 
            'tokens': ['FOR', '(', '1', '10', 'I', '(', 'I', 'PRINT', ')', ')'],
            'expected': True
        },
        
        # IF statement
        {
            'name': 'IF Statement',
            'tokens': ['IF', '(', '(', 'X', '5', '>', ')', '(', 'SUCCESS', 'PRINT', ')', ')'],
            'expected': True
        },
        
        # Erro: parênteses não balanceados
        {
            'name': 'Erro - Parênteses',
            'tokens': ['(', '3', '4', '+'],
            'expected': False
        },
        
        # Erro: operador sem operandos suficientes
        {
            'name': 'Erro - Operandos',
            'tokens': ['(', '3', '+', ')'],
            'expected': False
        }
    ]
    
    print("\n=== TESTANDO PARSER LL(1) ===")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Teste {i}: {test_case['name']} ---")
        print(f"Tokens: {test_case['tokens']}")
        
        resultado = parsear(test_case['tokens'], tabela_ll1)
        
        if resultado['success'] == test_case['expected']:
            print(f"✅ PASSOU: {test_case['name']}")
        else:
            print(f"❌ FALHOU: {test_case['name']}")
        
        if resultado['success']:
            print(f"📊 Tokens processados: {resultado['tokens_processed']}")
            print("🔧 Derivação:")
            for step in resultado['derivation'][-3:]:  # Últimos 3 passos
                print(f"   {step}")
        else:
            print(f"🚫 Erro: {resultado['error']}")
            print(f"💡 Sugestão: {resultado['recovery_suggestion']}")


def parsearComDebugging(tokens, tabela_ll1, verbose=True):
    """
    Versão com debugging detalhado para desenvolvimento.
    """
    if verbose:
        print("\n" + "="*60)
        print("🔍 PARSING LL(1) COM DEBUGGING DETALHADO")
        print("="*60)
    
    resultado = parsear(tokens, tabela_ll1)
    
    if verbose:
        print(f"\n📋 RESULTADO FINAL:")
        print(f"   Sucesso: {resultado['success']}")
        if resultado['success']:
            print(f"   Tokens processados: {resultado.get('tokens_processed', 0)}")
            print(f"   Passos de derivação: {len(resultado['derivation'])}")
        else:
            print(f"   Erro: {resultado['error']}")
            print(f"   Posição do erro: {resultado.get('position', 'N/A')}")
    
    return resultado


if __name__ == "__main__":
    testarParser()