#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import sys
import traceback
from pathlib import Path
from datetime import datetime

from src.RA1.functions.python.io_utils import lerArquivo
from src.RA1.functions.python.exibirResultados import exibirResultados
from src.RA1.functions.assembly import gerarAssemblyMultiple, save_assembly, save_registers_inc
from src.RA2.functions.python.gerarArvore import gerar_e_salvar_todas_arvores
from src.RA2.functions.python.lerTokens import lerTokens, validarTokens, reconhecerToken
from src.RA2.functions.python.construirGramatica import imprimir_gramatica_completa
from src.RA2.functions.python.construirTabelaLL1 import construirTabelaLL1
from src.RA2.functions.python.parsear import parsear_todas_linhas

# --- caminhos base do projeto ---
BASE_DIR    = Path(__file__).resolve().parent        # raiz do repo
INPUTS_DIR  = BASE_DIR / "inputs" / "RA1"                       # raiz/inputs
OUT_TOKENS  = BASE_DIR / "outputs" / "RA1" / "tokens" / "tokens_gerados.txt"
OUT_ASM_DIR = BASE_DIR / "outputs" / "RA1" / "assembly"          # raiz/outputs/assembly

# garante pastas de saída
OUT_ASM_DIR.mkdir(parents=True, exist_ok=True)
OUT_TOKENS.parent.mkdir(parents=True, exist_ok=True)

def atualizar_documentacao_gramatica():
    """Atualiza a seção Latest Syntax Tree no grammar_documentation.md com a última árvore gerada"""
    try:
        grammar_doc_path = BASE_DIR / "grammar_documentation.md"
        arvore_output_path = BASE_DIR / "arvore_output.txt"

        if not grammar_doc_path.exists():
            print(f"  Aviso: {grammar_doc_path} não encontrado, pulando atualização da documentação")
            return

        if not arvore_output_path.exists():
            print(f"  Aviso: {arvore_output_path} não encontrado, não é possível atualizar documentação")
            return

        # Lê o arquivo de árvores geradas
        with open(arvore_output_path, 'r', encoding='utf-8') as f:
            arvore_content = f.read()

        # Encontra a última árvore (busca pela última ocorrência de "LINHA")
        linhas = arvore_content.split('\n')
        ultima_arvore_inicio = -1
        ultima_linha_numero = ""

        for i, linha in enumerate(linhas):
            if linha.startswith('LINHA ') and linha.endswith(':'):
                ultima_arvore_inicio = i
                ultima_linha_numero = linha

        if ultima_arvore_inicio == -1:
            print("  Aviso: Nenhuma árvore encontrada no arquivo de saída")
            return

        # Extrai a última árvore completa
        arvore_lines = []
        arvore_lines.append(ultima_linha_numero)
        i = ultima_arvore_inicio + 1
        first_separator_passed = False

        # Adiciona as linhas da árvore até encontrar o separador final ou fim do arquivo
        while i < len(linhas):
            linha = linhas[i]
            arvore_lines.append(linha)

            # Se é um separador (linha de '===')
            if linha.startswith('=') and len(linha) >= 20:
                if not first_separator_passed:
                    # Este é o primeiro separador (que vem logo após "LINHA XX:")
                    first_separator_passed = True
                else:
                    # Este é o separador final da árvore
                    break
            i += 1

        ultima_arvore = '\n'.join(arvore_lines)

        # Lê o arquivo de documentação atual
        with open(grammar_doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()

        # Encontra a seção "Latest Syntax Tree" e substitui
        lines = doc_content.split('\n')
        new_lines = []
        in_syntax_tree_section = False

        for linha in lines:
            if linha.strip() == "## Latest Syntax Tree":
                new_lines.append(linha)
                in_syntax_tree_section = True

                # Adiciona timestamp e nova árvore
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_lines.append(f"\n*Last updated: {timestamp}*\n")
                new_lines.append("```")
                new_lines.append(ultima_arvore)
                new_lines.append("```")

                # Pula todas as linhas da seção anterior até encontrar próxima seção ou fim
                continue
            elif in_syntax_tree_section and linha.startswith('## '):
                # Nova seção encontrada, para de pular linhas
                in_syntax_tree_section = False
                new_lines.append(linha)
            elif not in_syntax_tree_section:
                new_lines.append(linha)

        # Escreve o arquivo atualizado
        updated_content = '\n'.join(new_lines)
        with open(grammar_doc_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"  Documentação grammar_documentation.md atualizada com árvore da {ultima_linha_numero}")

    except Exception as e:
        print(f"  Erro ao atualizar documentação: {e}")
        # Não interrompe a execução, apenas avisa

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO -> Especificar caminho do arquivo de teste (ex.: int/teste1.txt ou float/teste2.txt)")
        sys.exit(1)

    # --- resolve caminho da entrada ---
    arg = Path(sys.argv[1])

    # Ordem de prioridade para localizar arquivo:
    # 1. Caminho absoluto (se fornecido)
    # 2. Relativo ao diretório atual
    # 3. Relativo à raiz do projeto
    # 4. Dentro da pasta inputs/RA1 (padrão para testes)
    possibilidades = []
    
    if arg.is_absolute():
        possibilidades.append(arg)
    else:
        possibilidades.extend([
            Path.cwd() / arg,    # Relativo ao diretório atual
            BASE_DIR / arg,      # Relativo à raiz do projeto
            INPUTS_DIR / arg,    # Dentro da pasta inputs/RA1
        ])

    entrada = None
    for caminho in possibilidades:
        if caminho.exists():
            entrada = caminho.resolve()
            break

    if entrada is None:
        print(f"ERRO -> arquivo não encontrado: {arg}")
        print(f"Tentativas de busca:")
        for i, caminho in enumerate(possibilidades, 1):
            print(f"  {i}. {caminho}")
        sys.exit(1)

    operacoes_lidas = lerArquivo(str(entrada))

    # Exibe caminho relativo à raiz se possível (evita ValueError do relative_to)
    try:
        mostrar = entrada.relative_to(BASE_DIR)
    except ValueError:
        print("AVISO -> Não foi possível exibir o caminho relativo ao diretório base. Exibindo caminho absoluto.")
        mostrar = entrada
        
    print(f"\nArquivo de teste: {mostrar}\n")

    # Executa a análise das expressões RPN
    sucesso, linhas_processadas, linhas_com_erro = exibirResultados(operacoes_lidas, OUT_TOKENS)
    print("\n--- FIM DOS TESTES ---\n")
    
    # Se houve erros, interrompe a execução
    if not sucesso:
        print("EXECUÇÃO INTERROMPIDA:")
        print(f"   Foram encontrados {linhas_com_erro} erro(s) em {linhas_processadas} linha(s) processada(s).")
        print("   Corrija os erros antes de prosseguir com a geração de Assembly e análise sintática.")
        sys.exit(1)

    # --- Geração de código assembly para todas as operações em um único arquivo ---
    codigo_assembly = []

    # tokens foram salvos em raiz/outputs/tokens/tokens_gerados.txt
    linhas = lerArquivo(str(OUT_TOKENS))

    # Salvar registers.inc em ambos os locais
    save_registers_inc(str(OUT_ASM_DIR / "registers.inc"))  # Em RA1
    # save_registers_inc(str(BASE_DIR / "registers.inc"))  # Na raiz

    # Preparar lista de todas as operações (filtrar parênteses para assembly)
    all_tokens = []
    for linha in linhas:
        tokens = linha.split()
        # Filtrar parênteses apenas para geração de assembly (RA1 compatibility)
        tokens_sem_parenteses = [token for token in tokens if token not in ['(', ')']]
        all_tokens.append(tokens_sem_parenteses)

    # Gerar um único arquivo com todas as operações
    gerarAssemblyMultiple(all_tokens, codigo_assembly)
    
    # Salvar programa_completo.S em ambos os locais
    nome_arquivo_ra1 = OUT_ASM_DIR / "programa_completo.S"
    nome_arquivo_root = BASE_DIR / "programa_completo.S"
    
    save_assembly(codigo_assembly, str(nome_arquivo_ra1))  # Salva em RA1
    # save_assembly(codigo_assembly, str(nome_arquivo_root))  # Salva na raiz
    
    print(f"Arquivo {nome_arquivo_ra1.name} gerado com sucesso em:")
    print(f"- {OUT_ASM_DIR}")
    print(f"Contém {len(all_tokens)} operações RPN em sequência.")

    print("\nPara testar:")
    print("- Compile e carregue programa_completo.S no Arduino Uno")
    print("- Monitore a saída serial em 9600 baud para ver os resultados!")
    print("- Todas as operações serão executadas sequencialmente")


    ##################################################################
    # COMEÇO RA2
    ##################################################################

    # Leitura e validação dos tokens para análise sintática
    try:
        print("\n--- PROCESSAMENTO DE TOKENS PARA RA2 ---")
        tokens_para_ra2 = lerTokens(str(OUT_TOKENS))
        tokens_sao_validos = validarTokens(tokens_para_ra2)
        print(f"Tokens processados: {len(tokens_para_ra2)} tokens")
        print(f"Validação dos tokens: {'SUCESSO' if tokens_sao_validos else 'FALHOU'}")
    except Exception as e:
        print(f"  Erro no processamento de tokens: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Análise Sintática - Gramática
    try:
        print("\n--- ANALISE SINTATICA - GRAMATICA ---")
        imprimir_gramatica_completa()
    except Exception as e:
        print(f"  Erro ao exibir gramática: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Construção da tabela LL(1)
    try:
        print("\n--- CONSTRUÇÃO DA TABELA LL(1) ---")
        tabela_ll1 = construirTabelaLL1()
        print(f"  Tabela LL(1) construída com {len(tabela_ll1)} entradas")
    except Exception as e:
        print(f"  Erro ao construir tabela LL(1): {e}")
        traceback.print_exc()
        sys.exit(1)

    # Aplicação da análise sintática com parsear
    try:
        print("\n--- ANÁLISE SINTÁTICA COM PARSEAR ---")
        
        # Lê linha por linha do arquivo tokens_gerados.txt
        tokens_por_linha = []
        linhas_arquivo = lerArquivo(str(OUT_TOKENS))
        
        def segmentar_linha_em_instrucoes(linha_texto):
            """Segmenta uma linha em múltiplas instruções baseado em parênteses balanceados"""
            instrucoes = []
            elementos = linha_texto.split()
            i = 0
            
            while i < len(elementos):
                if elementos[i] == '(':
                    # Encontra expressão balanceada
                    instrucao_elementos = []
                    nivel_parenteses = 0
                    
                    while i < len(elementos):
                        elemento = elementos[i]
                        instrucao_elementos.append(elemento)
                        
                        if elemento == '(':
                            nivel_parenteses += 1
                        elif elemento == ')':
                            nivel_parenteses -= 1
                            
                        i += 1
                        
                        # Quando parênteses estão balanceados, temos uma instrução completa
                        if nivel_parenteses == 0:
                            break
                    
                    if instrucao_elementos:
                        instrucoes.append(' '.join(instrucao_elementos))
                else:
                    i += 1
            
            return instrucoes

        for linha_texto in linhas_arquivo:
            linha_texto = linha_texto.strip()
            if linha_texto and not linha_texto.startswith('#'):
                # Segmenta linha em múltiplas instruções se necessário
                instrucoes = segmentar_linha_em_instrucoes(linha_texto)
                
                for instrucao in instrucoes:
                    # Processa cada instrução individualmente usando lerTokens
                    tokens_linha = []
                    elementos = instrucao.split()
                    
                    for elemento in elementos: 
                        # Usa o reconhecerToken do lerTokens.py
                        token = reconhecerToken(elemento, 1, 1)  # linha e coluna fictícias
                        if token:
                            tokens_linha.append(token)
                    
                    if tokens_linha:
                        tokens_por_linha.append(tokens_linha)
        
        print(f"Analisando {len(tokens_por_linha)} linha(s) de tokens")
        
        # Aplica parsear para cada linha
        derivacoes = parsear_todas_linhas(tabela_ll1, tokens_por_linha)
        
        # Gera e salva todas as árvores sintáticas
        print("\n--- GERAÇÃO DAS ÁRVORES SINTÁTICAS ---")
        gerar_e_salvar_todas_arvores(derivacoes, "arvore_output.txt")

        # Atualiza a documentação da gramática com a última árvore gerada
        print("\n--- ATUALIZAÇÃO DA DOCUMENTAÇÃO ---")
        atualizar_documentacao_gramatica()
        
    except Exception as e:
        print(f"  Erro na análise sintática: {e}")
        traceback.print_exc()    