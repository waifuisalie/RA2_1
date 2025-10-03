#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import io
import sys
from pathlib import Path
from src.RA1.functions.python.rpn_calc import parseExpressao, executarExpressao
from src.RA1.functions.python.io_utils import salvar_tokens
from src.RA1.functions.python.tokens import Tipo_de_Token
from src.RA1.functions.python.validarExpressao import validarExpressao, criarMensagemErro

def exibirResultados(vetor_linhas: list[str], out_tokens: Path) -> tuple[bool, int, int]:
    
    memoria_global = {}
    tokens_salvos_txt = []
    contador_erros = 0
    linhas_processadas = 0

    # Inicializar o histórico na memória global
    memoria_global['historico_resultados'] = []

    for i, linha in enumerate(vetor_linhas, 1):
        # Pula linhas vazias ou comentários
        if not linha.strip() or linha.strip().startswith('#'):
            continue
        
        linhas_processadas += 1
        
        # Valida a expressão usando a função dedicada
        eh_valida, mensagem_erro = validarExpressao(linha, i)
        if not eh_valida:
            print(mensagem_erro)
            tokens_salvos_txt.append([])
            memoria_global['historico_resultados'].append(None)
            contador_erros += 1
            continue
            
        try:
            lista_de_tokens = parseExpressao(linha)
            # para salvar tokens completos (incluindo parênteses) para RA2
            tokens_completos = [str(token.valor) for token in lista_de_tokens if token.tipo != Tipo_de_Token.FIM]
            tokens_salvos_txt.append(tokens_completos)

            # Captura saída para detectar erros do RA1
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            try:
                resultado = executarExpressao(lista_de_tokens, memoria_global)
                sys.stdout = old_stdout
                
                # Verifica se houve erro capturado
                output = buffer.getvalue()
                if 'ERRO' in output:
                    print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")
                    # Formata o erro com indentação
                    erro_lines = output.strip().split('\n')
                    for erro_line in erro_lines:
                        if erro_line.strip():
                            print(f"    {erro_line}")
                    contador_erros += 1
                else:
                    print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")
                    
                memoria_global['historico_resultados'].append(resultado)
            except Exception as exec_error:
                sys.stdout = old_stdout
                raise exec_error
            
        except ValueError as e:
            print(criarMensagemErro(linha, i, "SINTAXE", str(e)))
            tokens_salvos_txt.append([])  # Adiciona lista vazia para manter índices
            memoria_global['historico_resultados'].append(None)  # Adiciona None para erro
            contador_erros += 1
            
        except ZeroDivisionError:
            print(criarMensagemErro(linha, i, "MATEMÁTICO", "Divisão por zero"))
            tokens_salvos_txt.append([])
            memoria_global['historico_resultados'].append(None)
            contador_erros += 1
            
        except Exception as e:
            print(criarMensagemErro(linha, i, "INESPERADO", f"{type(e).__name__}: {e}"))
            tokens_salvos_txt.append([])
            memoria_global['historico_resultados'].append(None)
            contador_erros += 1

    # Salva os tokens gerados
    salvar_tokens(tokens_salvos_txt, out_tokens)
    
    # Retorna (sucesso, linhas_processadas, contador_erros)
    return (contador_erros == 0, linhas_processadas, contador_erros)