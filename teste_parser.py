#!/usr/bin/env python3
"""
Arquivo de teste para o Parser LL(1)
Execute: python test_parser.py
"""

import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar funções necessárias
from .construirGramatica import construirGramatica
from .parsear import parsear, imprimir_derivacao, executar_todos_testes


def main():
    print("="*70)
    print(" TESTE DO PARSER LL(1) - RPN")
    print("="*70)
    
    # Opção 1: Executar bateria completa de testes
    print("\n[Executando bateria completa de testes...]\n")
    sucesso = executar_todos_testes()
    
    if sucesso:
        print("\n✓ Todos os testes passaram!")
    else:
        print("\n✗ Alguns testes falharam. Veja detalhes acima.")
    
    # Opção 2: Teste individual simples
    print("\n" + "="*70)
    print(" TESTE INDIVIDUAL: (3 2 +)")
    print("="*70)
    
    # Construir gramática
    print("\nConstruindo gramática...")
    gramatica_info = construirGramatica()
    
    if not gramatica_info['is_ll1']:
        print("ERRO: Gramática contém conflitos!")
        return
    
    print("✓ Gramática LL(1) válida")
    
    # Tokens de teste
    tokens = [
        ('(', '(', 1, 0),
        ('NUMBER', '3', 1, 1),
        ('NUMBER', '2', 1, 3),
        ('+', '+', 1, 5),
        (')', ')', 1, 6)
    ]
    
    print("\nExecutando parser...")
    resultado = parsear(tokens, gramatica_info['ll1_table_real'])
    
    if resultado['sucesso']:
        print("✓ Parsing bem-sucedido!\n")
        imprimir_derivacao(resultado['derivacao'])
    else:
        print(f"✗ Erro: {resultado['erro']}")


if __name__ == '__main__':
    main()