# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1

# ==================== tokens.py ====================

class Tipo_de_Token:
    """Tipos de tokens - comandos em inglês para integração com parser LL(1)"""
    
    # Números
    NUMBER = "NUMBER"
    
    # Operadores Aritméticos
    PLUS = "PLUS"               # +
    MINUS = "MINUS"             # -
    MULTIPLY = "MULTIPLY"       # *
    DIVIDE = "DIVIDE"           # /
    DIVIDE_REAL = "DIVIDE_REAL" # |
    MODULO = "MODULO"           # %
    POWER = "POWER"             # ^
    
    # Operadores Relacionais
    GREATER = "GREATER"         # >
    LESS = "LESS"               # <
    GREATER_EQUAL = "GTE"       # >=
    LESS_EQUAL = "LTE"          # <=
    EQUAL = "EQUAL"             # ==
    NOT_EQUAL = "NOT_EQUAL"     # !=
    
    # Símbolos de Agrupamento
    LPAREN = "LPAREN"           # (
    RPAREN = "RPAREN"           # )
    
    # Palavras-chave
    FOR = "FOR"
    WHILE = "WHILE"
    IF = "IF"
    ELSE = "ELSE"
    MEM = "MEM"
    RES = "RES"
    PRINT = "PRINT"
    
    # Identificadores
    IDENTIFIER = "IDENTIFIER"
    
    # Fim de arquivo
    EOF = "EOF"


class Token:
    """Representa um token com tipo e valor"""
    
    def __init__(self, tipo: str, valor, linha: int = 0, coluna: int = 0):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, L{self.linha}:C{self.coluna})"


# ==================== analisador_lexico.py ====================

class Analisador_Lexico:
    """
    Analisador Léxico para linguagem RPN com estruturas de controle.
    Fase 2 - Extensão completa com operadores relacionais e keywords.
    """
    
    def __init__(self, texto_fonte: str, numero_linha: int = 1):
        self.fonte = texto_fonte
        self.posicao = 0
        self.caractere_atual = self.fonte[self.posicao] if self.fonte else None
        self.linha = numero_linha
        self.coluna = 1
        
        # Palavras-chave reservadas (sem ASSIGN)
        self.palavras_chave = {
            'FOR': Tipo_de_Token.FOR,
            'WHILE': Tipo_de_Token.WHILE,
            'IF': Tipo_de_Token.IF,
            'ELSE': Tipo_de_Token.ELSE,
            'MEM': Tipo_de_Token.MEM,
            'RES': Tipo_de_Token.RES,
            'PRINT': Tipo_de_Token.PRINT
        }
    
    def avancar(self):
        """Avança para o próximo caractere"""
        self.posicao += 1
        self.coluna += 1
        
        if self.posicao < len(self.fonte):
            self.caractere_atual = self.fonte[self.posicao]
        else:
            self.caractere_atual = None
    
    def espiar(self, deslocamento=1):
        """Olha caractere à frente sem avançar"""
        pos_espiar = self.posicao + deslocamento
        if pos_espiar < len(self.fonte):
            return self.fonte[pos_espiar]
        return None
    
    def ignorar_espacos(self):
        """Ignora espaços em branco"""
        while self.caractere_atual is not None and self.caractere_atual.isspace():
            self.avancar()
    
    def analisar(self):
        """Analisa o texto e retorna lista de tokens"""
        tokens = []
        
        while self.caractere_atual is not None:
            token = self.obter_proximo_token()
            if token:
                tokens.append(token)
        
        # Adiciona token de fim
        tokens.append(Token(Tipo_de_Token.EOF, None, self.linha, self.coluna))
        return tokens
    
    def obter_proximo_token(self):
        """Obtém próximo token (máquina de estados)"""
        self.ignorar_espacos()
        
        if self.caractere_atual is None:
            return None
        
        # Números
        if self.caractere_atual.isdigit():
            return self.ler_numero()
        
        # Identificadores e palavras-chave
        if self.caractere_atual.isalpha():
            return self.ler_identificador()
        
        # Operadores e símbolos
        return self.ler_operador()
    
    def ler_numero(self):
        """Lê número inteiro ou real"""
        coluna_inicial = self.coluna
        string_numero = ""
        
        # Parte inteira
        while self.caractere_atual is not None and self.caractere_atual.isdigit():
            string_numero += self.caractere_atual
            self.avancar()
        
        # Parte decimal
        if self.caractere_atual == '.':
            string_numero += self.caractere_atual
            self.avancar()
            
            if not (self.caractere_atual and self.caractere_atual.isdigit()):
                raise ValueError(
                    f"Erro léxico L{self.linha}:C{self.coluna}: "
                    f"Esperado dígito após ponto decimal"
                )
            
            while self.caractere_atual is not None and self.caractere_atual.isdigit():
                string_numero += self.caractere_atual
                self.avancar()
        
        return Token(Tipo_de_Token.NUMBER, float(string_numero), self.linha, coluna_inicial)
    
    def ler_identificador(self):
        """Lê identificador ou palavra-chave"""
        coluna_inicial = self.coluna
        identificador = ""
        
        while self.caractere_atual is not None and self.caractere_atual.isalpha():
            identificador += self.caractere_atual
            self.avancar()
        
        # Verifica se é palavra-chave
        tipo_token = self.palavras_chave.get(identificador, Tipo_de_Token.IDENTIFIER)
        
        return Token(tipo_token, identificador, self.linha, coluna_inicial)
    
    def ler_operador(self):
        """Lê operadores e símbolos"""
        coluna_inicial = self.coluna
        char = self.caractere_atual
        
        # Parênteses
        if char == '(':
            self.avancar()
            return Token(Tipo_de_Token.LPAREN, '(', self.linha, coluna_inicial)
        
        if char == ')':
            self.avancar()
            return Token(Tipo_de_Token.RPAREN, ')', self.linha, coluna_inicial)
        
        # Operadores aritméticos simples
        if char == '+':
            self.avancar()
            return Token(Tipo_de_Token.PLUS, '+', self.linha, coluna_inicial)
        
        if char == '-':
            self.avancar()
            return Token(Tipo_de_Token.MINUS, '-', self.linha, coluna_inicial)
        
        if char == '*':
            self.avancar()
            return Token(Tipo_de_Token.MULTIPLY, '*', self.linha, coluna_inicial)
        
        if char == '/':
            self.avancar()
            return Token(Tipo_de_Token.DIVIDE, '/', self.linha, coluna_inicial)
        
        if char == '|':
            self.avancar()
            return Token(Tipo_de_Token.DIVIDE_REAL, '|', self.linha, coluna_inicial)
        
        if char == '%':
            self.avancar()
            return Token(Tipo_de_Token.MODULO, '%', self.linha, coluna_inicial)
        
        if char == '^':
            self.avancar()
            return Token(Tipo_de_Token.POWER, '^', self.linha, coluna_inicial)
        
        # Operadores relacionais compostos
        if char == '>':
            self.avancar()
            if self.caractere_atual == '=':
                self.avancar()
                return Token(Tipo_de_Token.GREATER_EQUAL, '>=', self.linha, coluna_inicial)
            return Token(Tipo_de_Token.GREATER, '>', self.linha, coluna_inicial)
        
        if char == '<':
            self.avancar()
            if self.caractere_atual == '=':
                self.avancar()
                return Token(Tipo_de_Token.LESS_EQUAL, '<=', self.linha, coluna_inicial)
            return Token(Tipo_de_Token.LESS, '<', self.linha, coluna_inicial)
        
        if char == '=':
            self.avancar()
            if self.caractere_atual == '=':
                self.avancar()
                return Token(Tipo_de_Token.EQUAL, '==', self.linha, coluna_inicial)
            raise ValueError(
                f"Erro léxico L{self.linha}:C{coluna_inicial}: "
                f"'=' sozinho inválido, use '=='"
            )
        
        if char == '!':
            self.avancar()
            if self.caractere_atual == '=':
                self.avancar()
                return Token(Tipo_de_Token.NOT_EQUAL, '!=', self.linha, coluna_inicial)
            raise ValueError(
                f"Erro léxico L{self.linha}:C{coluna_inicial}: "
                f"'!' sozinho inválido, use '!='"
            )
        
        # Caractere desconhecido
        raise ValueError(
            f"Erro léxico L{self.linha}:C{coluna_inicial}: "
            f"Caractere inválido '{char}'"
        )


# ==================== io_utils.py ====================

def lerArquivo(nome_arquivo: str):
    """Lê arquivo e retorna lista de linhas"""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado: {nome_arquivo}")
        return []
    except Exception as e:
        print(f"ERRO ao ler arquivo: {e}")
        return []


def salvarTokens(lista_tokens, arquivo_saida="tokens_saida.txt"):
    """Salva tokens em arquivo"""
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            for token in lista_tokens:
                f.write(f"{token}\n")
        return True
    except Exception as e:
        print(f"ERRO ao salvar tokens: {e}")
        return False


# ==================== lerTokens - Integração Fase 2 ====================

def lerTokens(nome_arquivo):
    """
    Função principal para Fase 2 - Responsabilidade do Aluno 3.
    Lê arquivo, tokeniza e retorna lista de TIPOS para o parser LL(1).
    
    Args:
        nome_arquivo: Nome do arquivo .txt com código RPN
        
    Returns:
        Lista de strings com tipos de tokens para o parser
    """
    linhas = lerArquivo(nome_arquivo)
    tokens_parser = []
    todos_tokens = []  # Para debug
    
    for num_linha, linha in enumerate(linhas, 1):
        if not linha:
            continue
        
        try:
            analisador = Analisador_Lexico(linha, num_linha)
            tokens = analisador.analisar()
            todos_tokens.extend(tokens)
            
            for token in tokens:
                if token.tipo == Tipo_de_Token.EOF:
                    continue
                
                # Mapear para formato do parser LL(1)
                if token.tipo == Tipo_de_Token.NUMBER:
                    tokens_parser.append('NUMBER')
                elif token.tipo == Tipo_de_Token.IDENTIFIER:
                    tokens_parser.append('IDENTIFIER')
                elif token.tipo == Tipo_de_Token.LPAREN:
                    tokens_parser.append('(')
                elif token.tipo == Tipo_de_Token.RPAREN:
                    tokens_parser.append(')')
                elif token.tipo == Tipo_de_Token.PLUS:
                    tokens_parser.append('+')
                elif token.tipo == Tipo_de_Token.MINUS:
                    tokens_parser.append('-')
                elif token.tipo == Tipo_de_Token.MULTIPLY:
                    tokens_parser.append('*')
                elif token.tipo == Tipo_de_Token.DIVIDE:
                    tokens_parser.append('/')
                elif token.tipo == Tipo_de_Token.DIVIDE_REAL:
                    tokens_parser.append('|')
                elif token.tipo == Tipo_de_Token.MODULO:
                    tokens_parser.append('%')
                elif token.tipo == Tipo_de_Token.POWER:
                    tokens_parser.append('^')
                elif token.tipo == Tipo_de_Token.GREATER:
                    tokens_parser.append('>')
                elif token.tipo == Tipo_de_Token.LESS:
                    tokens_parser.append('<')
                elif token.tipo == Tipo_de_Token.GREATER_EQUAL:
                    tokens_parser.append('>=')
                elif token.tipo == Tipo_de_Token.LESS_EQUAL:
                    tokens_parser.append('<=')
                elif token.tipo == Tipo_de_Token.EQUAL:
                    tokens_parser.append('==')
                elif token.tipo == Tipo_de_Token.NOT_EQUAL:
                    tokens_parser.append('!=')
                elif token.tipo == Tipo_de_Token.FOR:
                    tokens_parser.append('FOR')
                elif token.tipo == Tipo_de_Token.WHILE:
                    tokens_parser.append('WHILE')
                elif token.tipo == Tipo_de_Token.IF:
                    tokens_parser.append('IF')
                elif token.tipo == Tipo_de_Token.ELSE:
                    tokens_parser.append('ELSE')
                elif token.tipo == Tipo_de_Token.MEM:
                    tokens_parser.append('MEM')
                elif token.tipo == Tipo_de_Token.RES:
                    tokens_parser.append('RES')
                elif token.tipo == Tipo_de_Token.PRINT:
                    tokens_parser.append('PRINT')
        
        except ValueError as e:
            print(f"Erro léxico na linha {num_linha}: {e}")
            return None
    
    return tokens_parser


# ==================== TESTES ====================

def testar_analisador():
    """Testa o analisador léxico"""
    print("="*60)
    print("TESTANDO ANALISADOR LÉXICO - FASE 2")
    print("="*60)
    
    casos_teste = [
        ("(3 4 +)", "Expressão simples"),
        ("(10.5 3.2 *)", "Números reais"),
        ("(X Y >)", "Operador relacional"),
        ("FOR (1 10 I (I PRINT))", "Loop FOR"),
        ("IF ((A B ==) (SUCCESS PRINT))", "Condicional IF"),
        ("(15 3 |)", "Divisão real"),
        ("(X 5 >=)", "Maior ou igual"),
        ("(42 RESULT MEM)", "Atribuição com MEM"),
        ("(RESULT)", "Recuperar valor da memória"),
        ("(3 RES)", "Referência resultado anterior"),
    ]
    
    for fonte, descricao in casos_teste:
        print(f"\n{descricao}")
        print(f"Código: {fonte}")
        
        try:
            analisador = Analisador_Lexico(fonte)
            tokens = analisador.analisar()
            
            print("Tokens:")
            for token in tokens:
                if token.tipo != Tipo_de_Token.EOF:
                    print(f"  {token}")
            
            print("Para parser:")
            tokens_parser = []
            for token in tokens:
                if token.tipo == Tipo_de_Token.EOF:
                    continue
                if token.tipo == Tipo_de_Token.NUMBER:
                    tokens_parser.append('NUMBER')
                elif token.tipo == Tipo_de_Token.IDENTIFIER:
                    tokens_parser.append('IDENTIFIER')
                else:
                    tokens_parser.append(token.valor)
            print(f"  {tokens_parser}")
            
        except ValueError as e:
            print(f"ERRO: {e}")


if __name__ == "__main__":
    testar_analisador()elif token.type == TokenType.WHILE:
                    parser_tokens.append('WHILE')
                elif token.type == TokenType.IF:
                    parser_tokens.append('IF')
                elif token.type == TokenType.ELSE:
                    parser_tokens.append('ELSE')
                elif token.type == TokenType.ASSIGN:
                    parser_tokens.append('ASSIGN')
                elif token.type == TokenType.MEM:
                    parser_tokens.append('MEM')
                elif token.type == TokenType.RES:
                    parser_tokens.append('RES')
                elif token.type == TokenType.PRINT:
                    parser_tokens.append('PRINT')
        
        except ValueError as e:
            print(f"Erro léxico na linha {line_num}: {e}")
            return None
    
    return parser_tokens


# ==================== TESTES ====================

def test_lexer():
    """Testa o analisador léxico"""
    print("="*60)
    print("TESTANDO ANALISADOR LÉXICO - FASE 2")
    print("="*60)
    
    test_cases = [
        ("(3 4 +)", "Expressão simples"),
        ("(10.5 3.2 *)", "Números reais"),
        ("(X Y >)", "Operador relacional"),
        ("FOR (1 10 I (I PRINT))", "Loop FOR"),
        ("IF ((A B ==) (SUCCESS PRINT))", "Condicional IF"),
        ("(15 3 |)", "Divisão real"),
        ("(X 5 >=)", "Maior ou igual"),
        ("ASSIGN (42 RESULT)", "Atribuição"),
    ]
    
    for source, description in test_cases:
        print(f"\n{description}")
        print(f"Código: {source}")
        
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            print("Tokens:")
            for token in tokens:
                if token.type != TokenType.EOF:
                    print(f"  {token}")
            
            print("Para parser:")
            parser_tokens = []
            for token in tokens:
                if token.type == TokenType.EOF:
                    continue
                if token.type == TokenType.NUMBER:
                    parser_tokens.append('NUMBER')
                elif token.type == TokenType.IDENTIFIER:
                    parser_tokens.append('IDENTIFIER')
                else:
                    parser_tokens.append(token.value)
            print(f"  {parser_tokens}")
            
        except ValueError as e:
            print(f"ERRO: {e}")


if __name__ == "__main__":
    test_lexer()