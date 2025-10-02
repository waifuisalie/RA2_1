# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

"""
ALUNO 2: Função parsear e Parser Descendente Recursivo
=======================================================
Responsável por:
- Implementar parsear(tokens, tabela_ll1) para análise sintática
- Usar tabela LL(1) para guiar o parsing
- Implementar pilha de análise e controle de derivação
- Detectar e reportar erros sintáticos
- Gerar estrutura de derivação para a árvore sintática
"""

from typing import List, Dict, Tuple, Optional, Any

# ============================================================================
# CLASSE PARA REPRESENTAR TOKENS
# ============================================================================

class Token:
    """Representa um token do analisador léxico"""
    def __init__(self, tipo: str, valor: str, linha: int = 0, coluna: int = 0):
        self.tipo = tipo      # Tipo do token (NUMBER, IDENTIFIER, PLUS, etc)
        self.valor = valor    # Valor literal do token
        self.linha = linha    # Linha no código fonte
        self.coluna = coluna  # Coluna no código fonte
    
    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', L{self.linha}:C{self.coluna})"
    
    def __str__(self):
        return f"{self.tipo}('{self.valor}')"


# ============================================================================
# CLASSE PARA REPRESENTAR NÓS DA ÁRVORE SINTÁTICA
# ============================================================================

class NoArvore:
    """Representa um nó na árvore sintática (derivação)"""
    def __init__(self, simbolo: str, valor: Optional[str] = None, 
                 filhos: Optional[List['NoArvore']] = None):
        self.simbolo = simbolo    # Nome do símbolo (terminal ou não-terminal)
        self.valor = valor        # Valor do token (se for terminal)
        self.filhos = filhos if filhos is not None else []
        self.regra = None         # Número da regra aplicada (se não-terminal)
    
    def adicionar_filho(self, filho: 'NoArvore'):
        """Adiciona um filho ao nó"""
        self.filhos.append(filho)
    
    def __repr__(self):
        if self.valor:
            return f"NoArvore({self.simbolo}, '{self.valor}')"
        return f"NoArvore({self.simbolo}, {len(self.filhos)} filhos)"
    
    def to_dict(self) -> Dict:
        """Converte a árvore para dicionário (para JSON)"""
        resultado = {
            'simbolo': self.simbolo,
            'regra': self.regra
        }
        if self.valor:
            resultado['valor'] = self.valor
        if self.filhos:
            resultado['filhos'] = [filho.to_dict() for filho in self.filhos]
        return resultado


# ============================================================================
# CLASSE PARA ERROS SINTÁTICOS
# ============================================================================

class ErroSintatico(Exception):
    """Exceção personalizada para erros sintáticos"""
    def __init__(self, mensagem: str, token: Optional[Token] = None):
        self.mensagem = mensagem
        self.token = token
        super().__init__(self.formatar_erro())
    
    def formatar_erro(self) -> str:
        """Formata a mensagem de erro com informações do token"""
        if self.token:
            return (f"Erro Sintático na linha {self.token.linha}, "
                   f"coluna {self.token.coluna}:\n  {self.mensagem}\n"
                   f"  Token encontrado: {self.token}")
        return f"Erro Sintático: {self.mensagem}"


# ============================================================================
# CLASSE PARSER LL(1)
# ============================================================================

class ParserLL1:
    """Parser descendente recursivo LL(1)"""
    
    def __init__(self, tokens: List[Token], tabela_ll1: Dict[str, Dict[str, int]], 
                 gramatica: Dict[str, List[List[str]]]):
        """
        Inicializa o parser.
        
        Args:
            tokens: Lista de tokens do analisador léxico
            tabela_ll1: Tabela de parsing LL(1)
            gramatica: Regras de produção da gramática
        """
        self.tokens = tokens
        self.tabela_ll1 = tabela_ll1
        self.gramatica = gramatica
        self.posicao = 0
        self.token_atual = tokens[0] if tokens else None
        self.historico_derivacao = []  # Para rastrear derivações
        self.erros = []  # Lista de erros encontrados
    
    def avancar(self):
        """Avança para o próximo token"""
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
        else:
            # Token EOF
            self.token_atual = Token('EOF', '$', 
                                    self.tokens[-1].linha if self.tokens else 0,
                                    self.tokens[-1].coluna if self.tokens else 0)
    
    def olhar_frente(self, n: int = 1) -> Optional[Token]:
        """Olha n tokens à frente sem consumir"""
        pos = self.posicao + n
        if pos < len(self.tokens):
            return self.tokens[pos]
        return Token('EOF', '$', 0, 0)
    
    def consumir(self, tipo_esperado: str) -> Token:
        """
        Consome um token do tipo esperado.
        
        Args:
            tipo_esperado: Tipo do token esperado
            
        Returns:
            Token consumido
            
        Raises:
            ErroSintatico: Se o token não for do tipo esperado
        """
        if self.token_atual.tipo != tipo_esperado:
            raise ErroSintatico(
                f"Esperado '{tipo_esperado}', encontrado '{self.token_atual.tipo}'",
                self.token_atual
            )
        
        token = self.token_atual
        self.avancar()
        return token
    
    def registrar_derivacao(self, nao_terminal: str, numero_regra: int):
        """Registra uma derivação aplicada"""
        producao = self.gramatica[nao_terminal][numero_regra]
        self.historico_derivacao.append({
            'nao_terminal': nao_terminal,
            'regra': numero_regra,
            'producao': ' '.join(producao)
        })
    
    def parse_nao_terminal(self, nao_terminal: str) -> NoArvore:
        """
        Parseia um não-terminal usando a tabela LL(1).
        
        Args:
            nao_terminal: Nome do não-terminal a parsear
            
        Returns:
            Nó da árvore sintática representando a derivação
        """
        # Criar nó para este não-terminal
        no = NoArvore(nao_terminal)
        
        # Verificar se há entrada na tabela para (nao_terminal, token_atual)
        if nao_terminal not in self.tabela_ll1:
            raise ErroSintatico(
                f"Não-terminal '{nao_terminal}' não encontrado na tabela LL(1)",
                self.token_atual
            )
        
        entradas = self.tabela_ll1[nao_terminal]
        tipo_token = self.token_atual.tipo
        
        if tipo_token not in entradas:
            # Tentar recuperação de erro
            esperados = ', '.join(entradas.keys())
            raise ErroSintatico(
                f"Token inesperado para '{nao_terminal}'.\n"
                f"  Esperados: {esperados}\n"
                f"  Encontrado: {tipo_token}",
                self.token_atual
            )
        
        # Obter número da regra a aplicar
        numero_regra = entradas[tipo_token]
        producao = self.gramatica[nao_terminal][numero_regra]
        
        # Registrar derivação
        no.regra = numero_regra
        self.registrar_derivacao(nao_terminal, numero_regra)
        
        # Processar cada símbolo da produção
        for simbolo in producao:
            if simbolo == 'EPSILON':
                # Produção vazia (epsilon)
                filho = NoArvore('ε')
                no.adicionar_filho(filho)
                continue
            
            # Verificar se é terminal ou não-terminal
            if self.eh_terminal(simbolo):
                # Terminal: consumir token
                try:
                    token = self.consumir(simbolo)
                    filho = NoArvore(simbolo, token.valor)
                    no.adicionar_filho(filho)
                except ErroSintatico as e:
                    self.erros.append(e)
                    raise
            else:
                # Não-terminal: recursão
                try:
                    filho = self.parse_nao_terminal(simbolo)
                    no.adicionar_filho(filho)
                except ErroSintatico as e:
                    self.erros.append(e)
                    raise
        
        return no
    
    def eh_terminal(self, simbolo: str) -> bool:
        """Verifica se um símbolo é terminal"""
        terminais = {
            'LPAREN', 'RPAREN', 'NUMBER', 'IDENTIFIER',
            'PLUS', 'MINUS', 'MULT', 'DIV_REAL', 'DIV_INT', 'MOD', 'POW',
            'GT', 'LT', 'EQ', 'NEQ', 'GTE', 'LTE',
            'AND', 'OR', 'NOT',
            'MEM', 'RES', 'FOR', 'WHILE', 'IF', 'ELSE', 'EOF'
        }
        return simbolo in terminais
    
    def parsear(self) -> Tuple[bool, Optional[NoArvore], List[Dict]]:
        """
        Executa o parsing completo.
        
        Returns:
            Tupla contendo:
            - sucesso: True se parsing bem-sucedido
            - arvore: Raiz da árvore sintática (ou None se erro)
            - derivacoes: Lista de derivações aplicadas
        """
        try:
            # Começar pelo símbolo inicial
            arvore = self.parse_nao_terminal('PROGRAM')
            
            # Verificar se consumiu todos os tokens
            if self.token_atual.tipo != 'EOF':
                raise ErroSintatico(
                    f"Tokens restantes após parsing completo",
                    self.token_atual
                )
            
            print("✅ Parsing concluído com sucesso!")
            return True, arvore, self.historico_derivacao
            
        except ErroSintatico as e:
            print(f"❌ {e}")
            return False, None, self.historico_derivacao


# ============================================================================
# FUNÇÃO PRINCIPAL: parsear()
# ============================================================================

def parsear(tokens: List[Token], tabela_ll1: Dict[str, Dict[str, int]], 
           gramatica: Dict[str, List[List[str]]]) -> Tuple[bool, Optional[NoArvore], List[Dict]]:
    """
    ALUNO 2: Função principal de parsing sintático.
    
    Implementa um parser descendente recursivo LL(1) que:
    1. Usa a tabela LL(1) para decidir quais produções aplicar
    2. Constrói a árvore sintática durante o parsing
    3. Detecta e reporta erros sintáticos
    4. Gera histórico de derivações
    
    Args:
        tokens: Lista de tokens do analisador léxico
        tabela_ll1: Tabela de parsing LL(1) (de construirGramatica)
        gramatica: Regras de produção da gramática
        
    Returns:
        Tupla contendo:
        - sucesso: True se parsing foi bem-sucedido, False caso contrário
        - arvore: Raiz da árvore sintática (None se houver erro)
        - derivacoes: Lista de derivações aplicadas durante o parsing
    """
    if not tokens:
        print("❌ Erro: lista de tokens vazia")
        return False, None, []
    
    print(f"\nIniciando parsing de {len(tokens)} tokens...")
    print("=" * 80)
    
    # Criar parser e executar
    parser = ParserLL1(tokens, tabela_ll1, gramatica)
    sucesso, arvore, derivacoes = parser.parsear()
    
    # Exibir estatísticas
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DO PARSING:")
    print(f"  Tokens processados: {parser.posicao}")
    print(f"  Derivações aplicadas: {len(derivacoes)}")
    print(f"  Erros encontrados: {len(parser.erros)}")
    print("=" * 80)
    
    return sucesso, arvore, derivacoes


# ============================================================================
# FUNÇÕES AUXILIARES PARA VISUALIZAÇÃO
# ============================================================================

def exibir_derivacoes(derivacoes: List[Dict]):
    """Exibe o histórico de derivações de forma legível"""
    print("\nHISTÓRICO DE DERIVAÇÕES:")
    print("=" * 80)
    for i, derivacao in enumerate(derivacoes, 1):
        print(f"{i:3}. {derivacao['nao_terminal']:15} → {derivacao['producao']}")


def exibir_arvore(no: NoArvore, nivel: int = 0, prefixo: str = ""):
    """
    Exibe a árvore sintática de forma hierárquica.
    
    Args:
        no: Nó raiz da árvore
        nivel: Nível de indentação
        prefixo: Prefixo para o nó atual
    """
    if nivel == 0:
        print("\nÁRVORE SINTÁTICA:")
        print("=" * 80)
    
    # Exibir nó atual
    if no.valor:
        print(f"{prefixo}{no.simbolo}: '{no.valor}'")
    else:
        if no.regra is not None:
            print(f"{prefixo}{no.simbolo} (regra {no.regra})")
        else:
            print(f"{prefixo}{no.simbolo}")
    
    # Exibir filhos
    for i, filho in enumerate(no.filhos):
        eh_ultimo = (i == len(no.filhos) - 1)
        novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
        prefixo_filho = prefixo + ("└── " if eh_ultimo else "├── ")
        
        exibir_arvore(filho, nivel + 1, prefixo_filho)


# ============================================================================
# FUNÇÕES DE TESTE
# ============================================================================

def criar_tokens_teste(codigo: str) -> List[Token]:
    """
    Cria tokens de teste a partir de uma string de código.
    Simulação simplificada do analisador léxico.
    """
    tokens = []
    linha = 1
    
    # Mapeamento de símbolos para tipos de token
    mapa_tokens = {
        '(': 'LPAREN',
        ')': 'RPAREN',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULT',
        '|': 'DIV_REAL',
        '/': 'DIV_INT',
        '%': 'MOD',
        '^': 'POW',
        '>': 'GT',
        '<': 'LT',
        '==': 'EQ',
        '!=': 'NEQ',
        '>=': 'GTE',
        '<=': 'LTE',
        '&&': 'AND',
        '||': 'OR',
        '!': 'NOT',
        'MEM': 'MEM',
        'RES': 'RES',
        'FOR': 'FOR',
        'WHILE': 'WHILE',
        'IF': 'IF',
        'ELSE': 'ELSE'
    }
    
    palavras = codigo.split()
    for palavra in palavras:
        # Verificar se é símbolo conhecido
        if palavra in mapa_tokens:
            tokens.append(Token(mapa_tokens[palavra], palavra, linha))
        # Verificar se é número
        elif palavra.replace('.', '').replace('-', '').isdigit():
            tokens.append(Token('NUMBER', palavra, linha))
        # Senão, é identificador
        else:
            tokens.append(Token('IDENTIFIER', palavra, linha))
    
    return tokens


def testar_parser():
    """Função de teste do parser com exemplos válidos e inválidos"""
    print("\n" + "=" * 80)
    print("TESTES DO PARSER")
    print("=" * 80)
    
    # Importar gramática
    try:
        from construirGramatica import construirGramatica
        gramatica, first, follow, tabela_ll1 = construirGramatica()
    except ImportError as e:
        print(f"Erro ao importar: {e}")
        print("Certifique-se que o arquivo construirGramatica.py está no mesmo diretório")
        return
    
    # Testes
    testes = [
        # Teste 1: Expressão aritmética simples
        {
            'nome': 'Expressão aritmética simples',
            'codigo': '( 5 3 + )',
            'esperado': True
        },
        # Teste 2: Armazenamento em memória
        {
            'nome': 'Armazenamento em memória',
            'codigo': '( 8 X MEM )',
            'esperado': True
        },
        # Teste 3: Recuperar variável
        {
            'nome': 'Recuperar variável',
            'codigo': '( X )',
            'esperado': True
        },
        # Teste 4: Operação com variável
        {
            'nome': 'Operação com variável',
            'codigo': '( X 9 + )',
            'esperado': True
        },
        # Teste 5: Expressão aninhada
        {
            'nome': 'Expressão aninhada',
            'codigo': '( ( 5 3 + ) 2 * )',
            'esperado': True
        },
        # Teste 6: Erro - token inesperado
        {
            'nome': 'ERRO: Token inesperado',
            'codigo': '( 5 + 3 )',
            'esperado': False
        }
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n{'=' * 80}")
        print(f"TESTE {i}: {teste['nome']}")
        print(f"Código: {teste['codigo']}")
        print(f"{'=' * 80}")
        
        tokens = criar_tokens_teste(teste['codigo'])
        sucesso, arvore, derivacoes = parsear(tokens, tabela_ll1, gramatica)
        
        if sucesso == teste['esperado']:
            print(f"✅ Teste passou!")
        else:
            print(f"❌ Teste falhou!")
        
        if sucesso and arvore:
            exibir_derivacoes(derivacoes)
            exibir_arvore(arvore)


# ============================================================================
# EXECUÇÃO DOS TESTES
# ============================================================================

if __name__ == "__main__":
    testar_parser()