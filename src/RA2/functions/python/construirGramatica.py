#!/usr/bin/env python3

from .configuracaoGramatica import GRAMATICA_RPN, SIMBOLO_INICIAL, mapear_tokens_reais_para_teoricos
from .calcularFirst import calcularFirst
from .calcularFollow import calcularFollow
from .construirTabelaLL1 import construirTabelaLL1, ConflictError

def construirGramatica():
    # Usar gramática teórica para extrair estrutura (consistente com documento)
    gramatica_teorica = GRAMATICA_RPN
    simbolo_inicial = SIMBOLO_INICIAL
    
    # Extrai terminais e não-terminais da gramática TEÓRICA
    nao_terminais = set(gramatica_teorica.keys())
    terminais = set()
    
    # Coleta todos os símbolos terminais das produções TEÓRICAS
    for producoes in gramatica_teorica.values():
        for producao in producoes:
            for simbolo in producao:
                if simbolo not in nao_terminais and simbolo != 'EPSILON':
                    terminais.add(simbolo)
    
    
    # Calcular conjuntos usando tokens reais (para funcionamento interno)
    conjuntos_first_reais = calcularFirst()
    conjuntos_follow_reais = calcularFollow()
    
    # Mapear de volta para tokens teóricos (para exibição coerente)
    conjuntos_first = {nt: mapear_tokens_reais_para_teoricos(conjunto) 
                      for nt, conjunto in conjuntos_first_reais.items()}
    conjuntos_follow = {nt: mapear_tokens_reais_para_teoricos(conjunto) 
                       for nt, conjunto in conjuntos_follow_reais.items()}
    
    tabela_ll1 = None
    tabela_ll1_teorica = None
    conflitos = []
    eh_ll1 = False
    
    try:
        tabela_ll1_reais = construirTabelaLL1()
        tabela_ll1 = tabela_ll1_reais  # Para uso interno
        tabela_ll1_teorica = mapear_tokens_reais_para_teoricos(tabela_ll1_reais)  # Para exibição
        eh_ll1 = True
    except ConflictError as e:
        conflitos = [str(e)]
    
    # Converte gramática para formato de lista de produções (compatibilidade)
    producoes_lista = []
    for nt, producoes in gramatica_teorica.items():
        for producao in producoes:
            if producao == ['EPSILON']:
                producoes_lista.append(f"{nt} -> ε")
            else:
                producoes_lista.append(f"{nt} -> {' '.join(producao)}")
    
    # Estrutura completa de retorno
    resultado = {
        'productions': producoes_lista,
        'grammar_dict': gramatica_teorica,
        'first_sets': conjuntos_first,  # Tokens teóricos para exibição
        'follow_sets': conjuntos_follow,  # Tokens teóricos para exibição  
        'll1_table': tabela_ll1_teorica,  # Tokens teóricos para exibição
        'll1_table_real': tabela_ll1,  # Tokens reais para uso interno
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
        
        # Mostrar TODAS as entradas da tabela LL(1)
        table = gramatica['ll1_table']
        total_entries = 0
        
        for nt in sorted(table.keys()):
            for terminal in sorted(table[nt].keys()):
                if table[nt][terminal] is not None:
                    production = ' '.join(table[nt][terminal])
                    print(f"M[{nt}, {terminal}] = {nt} → {production}")
                    total_entries += 1
        
        print(f"\nTotal de entradas na tabela: {total_entries}")
    else:
        print("Erro na construção da Tabela LL(1)")
    
    if gramatica['conflicts']:
        print(f"\nCONFLITOS LL(1) DETECTADOS:")
        for i, conflito in enumerate(gramatica['conflicts'], 1):
            print(f"{i}. {conflito}")

