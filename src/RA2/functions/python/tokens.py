class Tipo_de_Token:
    
    NUMERO_REAL = "NUMERO_REAL"
    SOMA = "SOMA"                      # +
    SUBTRACAO = "SUBTRACAO"            # -
    MULTIPLICACAO = "MULT"             # *
    DIVISAO = "DIV"                    # / divisao inteira
    RESTO = "RESTO"                    # %
    POTENCIA = "POT"                   # ^
    ABRE_PARENTESES = "ABRE_PARENTESES" # (
    FECHA_PARENTESES = "FECHA_PARENTESES" # )
    RES = "RES"
    MEM = "MEM"
    FIM = "FIM"

    # Estruturas de controle
    FOR = "FOR"
    WHILE = "WHILE"
    IF = "IF"
    ELSE = "ELSE"
    ASSIGN = "ASSIGN"
    PRINT = "PRINT"

    # Operadores relacionais
    MAIOR = "MAIOR"                    # >
    MENOR = "MENOR"                    # <
    MAIOR_IGUAL = "MAIOR_IGUAL"        # >=
    MENOR_IGUAL = "MENOR_IGUAL"        # <=
    IGUAL = "IGUAL"                    # ==
    DIFERENTE = "DIFERENTE"            # !=

    # Fixed division operators (PORTUGUESE - matches RA1)
    DIVISAO_REAL = "DIVISAO_REAL"      # | (real division)
    # Keep DIVISAO = "DIV" for / (integer division)

    # Identifiers (PORTUGUESE - matches RA1 pattern)
    IDENTIFICADOR = "IDENTIFICADOR"    # Variable names

class Token:
    def __init__(self, tipo: str, valor, linha: int = 0, coluna: int = 0):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"
