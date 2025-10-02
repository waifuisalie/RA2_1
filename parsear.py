#!/usr/bin/env python3

from .configuracaoGramatica import SIMBOLO_INICIAL, MAPEAMENTO_TOKENS

class ErroSintatico(Exception):
    """Exceção customizada para erros sintáticos"""
    def __init__(self, mensagem, posicao=None, token=None):
        self.mensagem = mensagem
        self.posicao = posicao
        self.token = token
        super().__init__(self.mensagem)


class Parser:
    """Parser LL(1) Descendente Recursivo para RPN"""
    
    def __init__(self, tokens, tabela_ll1):
        """
        Inicializa o parser
        
        Args:
            tokens: Lista de tuplas (tipo_token, valor, linha, coluna)
            tabela_ll1: Tabela LL(1) gerada por construirTabelaLL1()
        """
        self.tokens = tokens + [('$', '$', -1, -1)]  # Adiciona marcador de fim
        self.posicao = 0
        self.tabela_ll1 = tabela_ll1
        self.derivacao = []
        self.pilha = []
        
        # Inicializa pilha com símbolo inicial e $
        self.pilha.append('$')
        self.pilha.append(SIMBOLO_INICIAL)
        
    def token_atual(self):
        """Retorna o token atual sem avançar"""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return ('$', '$', -1, -1)
    
    def avancar(self):
        """Avança para o próximo token"""
        if self.posicao < len(self.tokens) - 1:
            self.posicao += 1
    
    def reportar_erro(self, mensagem):
        """Reporta erro sintático com informações detalhadas"""
        token_tipo, token_valor, linha, coluna = self.token_atual()
        
        if linha >= 0:
            erro_msg = f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}"
            erro_msg += f"\nToken encontrado: {token_tipo} ('{token_valor}')"
        else:
            erro_msg = f"Erro sintático: {mensagem}"
            erro_msg += f"\nToken encontrado: {token_tipo}"
        
        # Mostra contexto da pilha
        if len(self.pilha) > 1:
            erro_msg += f"\nEsperado: {self.pilha[-1]}"
        
        raise ErroSintatico(erro_msg, self.posicao, token_tipo)
    
    def parsear(self):
        """
        Executa o parsing LL(1) usando a pilha
        
        Returns:
            Lista de derivações (strings no formato "NT -> produção")
        """
        while len(self.pilha) > 0:
            topo = self.pilha[-1]
            token_tipo, token_valor, linha, coluna = self.token_atual()
            
            # Caso 1: Topo é '$' (fim esperado)
            if topo == '$':
                if token_tipo == '$':
                    self.pilha.pop()
                    return self.derivacao
                else:
                    self.reportar_erro(f"Esperado fim da entrada, mas encontrado '{token_valor}'")
            
            # Caso 2: Topo é EPSILON (produção vazia)
            elif topo == 'EPSILON':
                self.pilha.pop()
                continue
            
            # Caso 3: Topo é um terminal
            elif topo not in self.tabela_ll1:
                # Terminal - deve casar com token atual
                if topo == token_tipo or topo == token_valor:
                    self.pilha.pop()
                    self.avancar()
                else:
                    self.reportar_erro(f"Esperado '{topo}', mas encontrado '{token_valor}'")
            
            # Caso 4: Topo é um não-terminal
            else:
                # Consulta tabela LL(1)
                if token_tipo not in self.tabela_ll1[topo]:
                    # Tenta com o valor do token também
                    if token_valor not in self.tabela_ll1[topo]:
                        tokens_esperados = [t for t in self.tabela_ll1[topo].keys() 
                                          if self.tabela_ll1[topo][t] is not None]
                        self.reportar_erro(
                            f"Token inesperado. Esperado um de: {', '.join(tokens_esperados)}"
                        )
                    terminal_key = token_valor
                else:
                    terminal_key = token_tipo
                
                producao = self.tabela_ll1[topo][terminal_key]
                
                if producao is None:
                    tokens_esperados = [t for t in self.tabela_ll1[topo].keys() 
                                      if self.tabela_ll1[topo][t] is not None]
                    self.reportar_erro(
                        f"Entrada inválida. Esperado um de: {', '.join(tokens_esperados)}"
                    )
                
                # Remove não-terminal do topo
                self.pilha.pop()
                
                # Registra derivação (convertendo para tokens teóricos para exibição)
                producao_str = self._converter_producao_para_exibicao(producao)
                derivacao_str = f"{topo} → {producao_str}"
                self.derivacao.append(derivacao_str)
                
                # Empilha produção na ordem reversa (exceto EPSILON)
                if producao != ['EPSILON']:
                    for simbolo in reversed(producao):
                        self.pilha.append(simbolo)
        
        return self.derivacao
    
    def _converter_producao_para_exibicao(self, producao):
        """Converte produção com tokens reais para formato de exibição"""
        # Cria mapeamento inverso
        mapeamento_inverso = {v: k for k, v in MAPEAMENTO_TOKENS.items()}
        
        simbolos_exibicao = []
        for simbolo in producao:
            if simbolo == 'EPSILON':
                simbolos_exibicao.append('ε')
            else:
                # Tenta mapear de volta para token teórico
                simbolo_teorico = mapeamento_inverso.get(simbolo, simbolo)
                simbolos_exibicao.append(simbolo_teorico)
        
        return ' '.join(simbolos_exibicao)


def parsear(tokens, tabela_ll1):
    """
    Função principal de parsing LL(1)
    
    Args:
        tokens: Lista de tuplas (tipo_token, valor, linha, coluna)
                Formato esperado da Fase 1: [('NUMBER', '3.14', 1, 0), ...]
        tabela_ll1: Tabela LL(1) gerada por construirTabelaLL1()
                    Formato: {nt: {terminal: [producao]}}
    
    Returns:
        dict: {
            'sucesso': bool,
            'derivacao': lista de strings com derivações,
            'erro': string de erro (se houver)
        }
    """
    try:
        parser = Parser(tokens, tabela_ll1)
        derivacao = parser.parsear()
        
        return {
            'sucesso': True,
            'derivacao': derivacao,
            'erro': None
        }
    
    except ErroSintatico as e:
        return {
            'sucesso': False,
            'derivacao': parser.derivacao if hasattr(parser, 'derivacao') else [],
            'erro': str(e)
        }
    
    except Exception as e:
        return {
            'sucesso': False,
            'derivacao': [],
            'erro': f"Erro inesperado no parser: {str(e)}"
        }


def validar_tokens(tokens):
    """
    Valida formato básico dos tokens antes do parsing
    
    Args:
        tokens: Lista de tokens para validar
    
    Returns:
        tuple: (bool válido, string mensagem_erro)
    """
    if not isinstance(tokens, list):
        return False, "Tokens devem ser uma lista"
    
    if len(tokens) == 0:
        return False, "Lista de tokens vazia"
    
    for i, token in enumerate(tokens):
        if not isinstance(token, tuple) or len(token) < 2:
            return False, f"Token na posição {i} tem formato inválido. Esperado (tipo, valor, linha, coluna)"
    
    return True, "Tokens válidos"


def imprimir_derivacao(derivacao, arquivo_saida=None):
    """
    Imprime a derivação passo a passo
    
    Args:
        derivacao: Lista de strings com as derivações
        arquivo_saida: Arquivo opcional para salvar a derivação
    """
    print("\n=== Derivação LL(1) ===\n")
    
    for i, passo in enumerate(derivacao, 1):
        linha = f"{i:3}. {passo}"
        print(linha)
        
        if arquivo_saida:
            arquivo_saida.write(linha + '\n')
    
    print(f"\nTotal de passos de derivação: {len(derivacao)}")


# ============================================================================
# FUNÇÕES DE TESTE PARA VALIDAÇÃO DO PARSER
# ============================================================================

def testar_expressao_simples():
    """Teste 1: Expressão aritmética simples (3 2 +)"""
    print("\n" + "="*60)
    print("TESTE 1: Expressão Simples")
    print("="*60)
    
    # Tokens simulados para (3 2 +)
    tokens = [
        ('(', '(', 1, 0),
        ('NUMBER', '3', 1, 1),
        ('NUMBER', '2', 1, 3),
        ('+', '+', 1, 5),
        (')', ')', 1, 6)
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if resultado['sucesso']:
        print("✓ Parsing bem-sucedido!")
        imprimir_derivacao(resultado['derivacao'])
    else:
        print(f"✗ Erro: {resultado['erro']}")
    
    return resultado['sucesso']


def testar_expressao_aninhada():
    """Teste 2: Expressão aninhada ((3 2 +) 5 *)"""
    print("\n" + "="*60)
    print("TESTE 2: Expressão Aninhada")
    print("="*60)
    
    tokens = [
        ('(', '(', 1, 0),
        ('(', '(', 1, 1),
        ('NUMBER', '3', 1, 2),
        ('NUMBER', '2', 1, 4),
        ('+', '+', 1, 6),
        (')', ')', 1, 7),
        ('NUMBER', '5', 1, 9),
        ('*', '*', 1, 11),
        (')', ')', 1, 12)
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if resultado['sucesso']:
        print("✓ Parsing bem-sucedido!")
        imprimir_derivacao(resultado['derivacao'])
    else:
        print(f"✗ Erro: {resultado['erro']}")
    
    return resultado['sucesso']


def testar_comando_res():
    """Teste 3: Comando especial (2 RES)"""
    print("\n" + "="*60)
    print("TESTE 3: Comando RES")
    print("="*60)
    
    tokens = [
        ('(', '(', 1, 0),
        ('NUMBER', '2', 1, 1),
        ('RES', 'RES', 1, 3),
        (')', ')', 1, 6)
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if resultado['sucesso']:
        print("✓ Parsing bem-sucedido!")
        imprimir_derivacao(resultado['derivacao'])
    else:
        print(f"✗ Erro: {resultado['erro']}")
    
    return resultado['sucesso']


def testar_uso_memoria():
    """Teste 4: Uso de memória (X)"""
    print("\n" + "="*60)
    print("TESTE 4: Uso de Memória")
    print("="*60)
    
    tokens = [
        ('(', '(', 1, 0),
        ('IDENTIFIER', 'X', 1, 1),
        (')', ')', 1, 2)
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if resultado['sucesso']:
        print("✓ Parsing bem-sucedido!")
        imprimir_derivacao(resultado['derivacao'])
    else:
        print(f"✗ Erro: {resultado['erro']}")
    
    return resultado['sucesso']


def testar_erro_sintatico():
    """Teste 5: Erro sintático (3 + 2) - ordem inválida"""
    print("\n" + "="*60)
    print("TESTE 5: Erro Sintático (ordem inválida)")
    print("="*60)
    
    tokens = [
        ('(', '(', 1, 0),
        ('NUMBER', '3', 1, 1),
        ('+', '+', 1, 3),
        ('NUMBER', '2', 1, 5),
        (')', ')', 1, 6)
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if not resultado['sucesso']:
        print("✓ Erro detectado corretamente!")
        print(f"Mensagem: {resultado['erro']}")
    else:
        print("✗ Erro não foi detectado (falha no teste)")
    
    return not resultado['sucesso']


def testar_parenteses_desbalanceados():
    """Teste 6: Parênteses desbalanceados"""
    print("\n" + "="*60)
    print("TESTE 6: Parênteses Desbalanceados")
    print("="*60)
    
    tokens = [
        ('(', '(', 1, 0),
        ('NUMBER', '3', 1, 1),
        ('NUMBER', '2', 1, 3),
        ('+', '+', 1, 5)
        # Falta ')' no final
    ]
    
    from .construirGramatica import construirGramatica
    gramatica_info = construirGramatica()
    
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if not resultado['sucesso']:
        print("✓ Erro detectado corretamente!")
        print(f"Mensagem: {resultado['erro']}")
    else:
        print("✗ Erro não foi detectado (falha no teste)")
    
    return not resultado['sucesso']


def executar_todos_testes():
    """Executa todos os testes do parser"""
    print("\n" + "="*70)
    print(" BATERIA DE TESTES DO PARSER LL(1)")
    print("="*70)
    
    testes = [
        ("Expressão Simples", testar_expressao_simples),
        ("Expressão Aninhada", testar_expressao_aninhada),
        ("Comando RES", testar_comando_res),
        ("Uso de Memória", testar_uso_memoria),
        ("Erro Sintático", testar_erro_sintatico),
        ("Parênteses Desbalanceados", testar_parenteses_desbalanceados)
    ]
    
    resultados = []
    for nome, teste_fn in testes:
        try:
            passou = teste_fn()
            resultados.append((nome, passou))
        except Exception as e:
            print(f"\n✗ Exceção no teste '{nome}': {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "="*70)
    print(" RESUMO DOS TESTES")
    print("="*70)
    
    passou_total = sum(1 for _, passou in resultados if passou)
    total = len(resultados)
    
    for nome, passou in resultados:
        status = "✓ PASSOU" if passou else "✗ FALHOU"
        print(f"{status:12} - {nome}")
    
    print(f"\nResultado: {passou_total}/{total} testes passaram")
    
    return passou_total == total