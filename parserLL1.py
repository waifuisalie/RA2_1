# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1


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
        from construirGramatica import construirGramatica
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