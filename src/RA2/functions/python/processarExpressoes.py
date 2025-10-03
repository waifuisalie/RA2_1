#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Integrantes do grupo (ordem alfabetica):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenco Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import os
from typing import List, Dict
from src.RA1.functions.python.tokens import Token
from .agruparTokens import agrupar_tokens_por_expressao, extrair_texto_expressao
from .parsear import parsear
from .gerarArvore import gerarArvore, NoArvore


def processar_e_exportar_arvores(
    tokens_completos: List[Token],
    tabela_ll1: Dict,
    output_dir: str = "outputs/RA2",
    verbose: bool = False
) -> List[NoArvore]:
    """
    Processa tokens agrupando por expressao, gera arvore para cada uma e exporta.

    Args:
        tokens_completos: Lista completa de tokens do arquivo
        tabela_ll1: Tabela LL(1) para parsing
        output_dir: Diretorio de saida para arquivos
        verbose: Se True, mostra debug do parsing

    Returns:
        Lista de arvores sintáticas (uma por expressao)
    """
    # Agrupa tokens por expressao
    expressoes = agrupar_tokens_por_expressao(tokens_completos)

    print(f"\n{'='*60}")
    print(f"PROCESSAMENTO DE ARVORES SINTATICAS")
    print(f"{'='*60}")
    print(f"Total de expressoes encontradas: {len(expressoes)}\n")

    arvores = []

    # Processa cada expressao separadamente
    for i, tokens_expressao in enumerate(expressoes, 1):
        texto_expressao = extrair_texto_expressao(tokens_expressao)

        print(f"\n{'='*60}")
        print(f"EXPRESSAO {i}: {texto_expressao}")
        print(f"{'='*60}")

        try:
            # Parseia usando LINHA como simbolo inicial (nao PROGRAM)
            derivacao = parsear(
                tokens_expressao,
                tabela_ll1,
                simbolo_inicial='LINHA',
                verbose=verbose
            )

            # Gera arvore sintatica (usando LINHA como simbolo inicial)
            arvore = gerarArvore(derivacao, simbolo_inicial='LINHA')
            arvores.append(arvore)

            # Mostra arvore
            print(f"\nArvore Sintatica da Expressao {i}:\n")
            print(arvore.label)
            for j, filho in enumerate(arvore.filhos):
                eh_ultimo = j == len(arvore.filhos) - 1
                print(filho.desenhar_ascii('', eh_ultimo))

            print(f"\n[OK] Expressao {i} processada com sucesso!")

        except Exception as e:
            print(f"\n[ERRO] Falha ao processar expressao {i}: {e}")
            arvores.append(None)

    # Exporta todas as arvores em um unico arquivo
    exportar_arvores_consolidadas(arvores, expressoes, output_dir)

    return arvores


def exportar_arvores_consolidadas(
    arvores: List[NoArvore],
    expressoes: List[List[Token]],
    output_dir: str = "outputs/RA2"
):
    """
    Exporta todas as arvores em um unico arquivo com secoes separadas.

    Args:
        arvores: Lista de arvores sintaticas
        expressoes: Lista de tokens de cada expressao
        output_dir: Diretorio de saida
    """
    # Cria diretorio se nao existe
    os.makedirs(output_dir, exist_ok=True)

    # Arquivo consolidado
    output_path = os.path.join(output_dir, "arvore_output.txt")

    conteudo = []
    conteudo.append("=" * 70)
    conteudo.append("ARVORES SINTATICAS - TODAS AS EXPRESSOES")
    conteudo.append("=" * 70)
    conteudo.append(f"\nTotal de expressoes: {len(arvores)}\n")

    for i, (arvore, tokens_expr) in enumerate(zip(arvores, expressoes), 1):
        texto_expr = extrair_texto_expressao(tokens_expr)

        conteudo.append("\n" + "=" * 70)
        conteudo.append(f"EXPRESSAO {i}: {texto_expr}")
        conteudo.append("=" * 70 + "\n")

        if arvore:
            conteudo.append(arvore.label)
            for j, filho in enumerate(arvore.filhos):
                eh_ultimo = j == len(arvore.filhos) - 1
                conteudo.append(filho.desenhar_ascii('', eh_ultimo).rstrip())
        else:
            conteudo.append("[ERRO: Arvore nao gerada]")

        conteudo.append("")  # Linha em branco

    # Salva arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(conteudo))

    # Tambem salva na raiz
    root_path = "arvore_output.txt"
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(conteudo))

    print(f"\n{'='*60}")
    print(f"EXPORTACAO CONCLUIDA")
    print(f"{'='*60}")
    print(f"Arquivo gerado:")
    print(f"  - {root_path}")
    print(f"  - {output_path}")
    print(f"\nTotal de arvores exportadas: {len([a for a in arvores if a is not None])}/{len(arvores)}")
