from src.functions.gerarArvore import gerarArvore, exportar_arvore_ascii

if __name__ == "__main__":
    # Derivação de teste
    derivacao_exemplo = [
        'PROGRAM → STATEMENT_LIST',
        'STATEMENT_LIST → STATEMENT STATEMENT_LIST',
        'STATEMENT → IF_STATEMENT',
        'IF_STATEMENT → if ( CONDITION ) then STATEMENT',
        'CONDITION → OPERAND COMPARISON OPERAND',
        'OPERAND → IDENTIFIER',
        'COMPARISON → <',
        'OPERAND → NUMBER',
        'STATEMENT → ASSIGNMENT',
        'ASSIGNMENT → IDENTIFIER = EXPRESSION ;',
        'IDENTIFIER → x',
        'EXPRESSION → OPERAND OPERATOR OPERAND',
        'OPERAND → IDENTIFIER',
        'OPERATOR → +',
        'OPERAND → NUMBER',
        'STATEMENT_LIST → ε'
    ]


    arvore = gerarArvore(derivacao_exemplo)

    print("\nÁrvore Sintática:\n")
    print(arvore.label)
    for i, filho in enumerate(arvore.filhos):
        eh_ultimo = i == len(arvore.filhos) - 1
        print(filho.desenhar_ascii('', eh_ultimo))

    exportar_arvore_ascii(arvore)
