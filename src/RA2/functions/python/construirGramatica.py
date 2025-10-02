#!/usr/bin/env python3

from .configuracaoGramatica import GRAMATICA_RPN, SIMBOLO_INICIAL
from .calcularFirst import calcularFirst
from .calcularFollow import calcularFollow
from .construirTabelaLL1 import construirTabelaLL1, ConflictError

def construirGramatica():

    gramatica = GRAMATICA_RPN
    simbolo_inicial = SIMBOLO_INICIAL
    
    # Extrai terminais e não-terminais
    nao_terminais = set(gramatica.keys())
    terminais = set()
    
    # Coleta todos os símbolos terminais das produções
    for producoes in gramatica.values():
        for producao in producoes:
            for simbolo in producao:
                if simbolo not in nao_terminais and simbolo != 'EPSILON':
                    terminais.add(simbolo)
    
    
    # print("Calculando conjuntos FIRST...")
    conjuntos_first = calcularFirst()
    
    # print("Calculando conjuntos FOLLOW...")
    conjuntos_follow = calcularFollow()
    
    # print("Construindo tabela LL(1)...")
    tabela_ll1 = None
    conflitos = []
    eh_ll1 = False
    
    try:
        tabela_ll1 = construirTabelaLL1()
        eh_ll1 = True
    except ConflictError as e:
        conflitos = [str(e)]
    
    # Converte gramática para formato de lista de produções (compatibilidade)
    producoes_lista = []
    for nt, producoes in gramatica.items():
        for producao in producoes:
            if producao == ['EPSILON']:
                producoes_lista.append(f"{nt} -> ε")
            else:
                producoes_lista.append(f"{nt} -> {' '.join(producao)}")
    
    # Estrutura completa de retorno
    resultado = {
        'productions': producoes_lista,
        'grammar_dict': gramatica,
        'first_sets': conjuntos_first,
        'follow_sets': conjuntos_follow,
        'll1_table': tabela_ll1,
        'start_symbol': simbolo_inicial,
        'terminals': terminais,
        'non_terminals': nao_terminais,
        'conflicts': conflitos,
        'is_ll1': eh_ll1
    }
    
    return resultado


def imprimir_gramatica_completa():
    gramatica = construirGramatica()
    
    print(f"\n---- Estrutura da Gramática ----")
    print(f"\n- Símbolo Inicial: \n  {gramatica['start_symbol']}")
    
    print(f"\n- Símbolos Não-Terminais:")
    non_terminals = sorted(list(gramatica['non_terminals']))
    print(f"  {{{', '.join(non_terminals)}}}")
    
    print(f"\n- Símbolos Terminais:")
    terminals = sorted(list(gramatica['terminals']))
    print(f"  {{{', '.join(terminals)}}}")
    
    print(f"\n- Regras de Produção:")
    for i, producao in enumerate(gramatica['productions'], 1):
        print(f"{i:2}. {producao}")
    
    print(f"\n- Conjuntos First:")
    for nt in sorted(gramatica['first_sets'].keys()):
        first_set = gramatica['first_sets'][nt]
        symbols = sorted(list(first_set)) if first_set else ['∅']
        print(f"FIRST({nt}) = {{{', '.join(symbols)}}}")
    
    print(f"\n- Conjuntos Follow:")
    for nt in sorted(gramatica['follow_sets'].keys()):
        follow_set = gramatica['follow_sets'][nt]
        symbols = sorted(list(follow_set)) if follow_set else ['∅']
        print(f"FOLLOW({nt}) = {{{', '.join(symbols)}}}")
    
    print(f"\n- Tabela LL1:")
    if gramatica['ll1_table']:
        print("Tabela LL(1) construída com sucesso!")
        # Mostrar algumas entradas da tabela como exemplo
        table = gramatica['ll1_table']
        count = 0
        for nt in sorted(table.keys()):
            for terminal in sorted(table[nt].keys()):
                if table[nt][terminal] is not None and count < 5:
                    production = ' '.join(table[nt][terminal])
                    print(f"M[{nt}, {terminal}] = {nt} → {production}")
                    count += 1
            if count >= 5:
                break
        print(f"... (Total: {sum(1 for nt in table for t in table[nt] if table[nt][t] is not None)} entradas)")
    else:
        print("Erro na construção da Tabela LL(1)")
    
    if gramatica['conflicts']:
        print(f"\nCONFLITOS LL(1) DETECTADOS:")
        for i, conflito in enumerate(gramatica['conflicts'], 1):
            print(f"{i}. {conflito}")

