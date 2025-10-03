#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

import re

def validarExpressao(linha: str, numero_linha: int) -> tuple[bool, str]:
    
    linha = linha.strip()
    
    # Pula linhas vazias ou comentários
    if not linha or linha.startswith('#'):
        return True, ""
    
    # 1. Validação básica de parênteses
    abertura = linha.count('(')
    fechamento = linha.count(')')
    if abertura != fechamento:
        if abertura > fechamento:
            erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
            erro += f"    ERRO DE SINTAXE: Parênteses desbalanceados - faltam {abertura - fechamento} parêntese(s) de fechamento ')'"
        else:
            erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
            erro += f"    ERRO DE SINTAXE: Parênteses desbalanceados - faltam {fechamento - abertura} parêntese(s) de abertura '('"
        return False, erro
    
    # Remove parênteses e divide em tokens para análise
    tokens_para_analise = linha.replace('(', ' ').replace(')', ' ').split()
    operadores = ['+', '-', '*', '/', '%', '^', '<', '>', '==', '<=', '>=', '!=', '&&', '||', '!']
    comandos_especiais = ['WHILE', 'FOR', 'IFELSE', 'MEM', 'RES']
    
    # 2. Validação específica para estruturas de controle incompletas
    if 'IFELSE' in tokens_para_analise:
        # IFELSE pode ter parênteses aninhados, então usamos uma validação mais flexível
        # Verifica se há pelo menos 3 grupos de parênteses após IFELSE
        ifelse_pattern = r'^\(IFELSE\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\)$'
        if not re.match(ifelse_pattern, linha):
            # Validação mais simples: contar grupos de parênteses após IFELSE
            resto_linha = linha[linha.find('IFELSE')+6:].strip()
            if resto_linha.count('(') < 3 or resto_linha.count(')') < 3:
                erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
                erro += f"    ERRO DE SINTAXE: Estrutura IFELSE incompleta - formato esperado: IFELSE (condição)(verdadeiro)(falso)"
                return False, erro
    
    if 'WHILE' in tokens_para_analise:
        # WHILE pode ter parênteses aninhados
        while_pattern = r'^\(WHILE\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\)$'
        if not re.match(while_pattern, linha):
            # Validação mais simples: contar grupos de parênteses após WHILE  
            resto_linha = linha[linha.find('WHILE')+5:].strip()
            if resto_linha.count('(') < 2 or resto_linha.count(')') < 2:
                erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
                erro += f"    ERRO DE SINTAXE: Estrutura WHILE incompleta - formato esperado: WHILE (condição)(corpo)"
                return False, erro
    
    if 'FOR' in tokens_para_analise:
        # FOR pode ter parênteses aninhados
        for_pattern = r'^\(FOR\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\)$'
        if not re.match(for_pattern, linha):
            # Validação mais simples: contar grupos de parênteses após FOR
            resto_linha = linha[linha.find('FOR')+3:].strip()
            if resto_linha.count('(') < 4 or resto_linha.count(')') < 4:
                erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
                erro += f"    ERRO DE SINTAXE: Estrutura FOR incompleta - formato esperado: FOR (inicio)(fim)(incremento)(corpo)"
                return False, erro
    
    # 3. Verifica expressões vazias
    if not tokens_para_analise:
        erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
        erro += f"    ERRO DE SINTAXE: Expressão vazia"
        return False, erro
    
    # 4. Verifica operador isolado
    if len(tokens_para_analise) == 1 and tokens_para_analise[0] in operadores:
        erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
        erro += f"    ERRO DE SINTAXE: Operador '{tokens_para_analise[0]}' sem operandos"
        return False, erro
    
    # 5. Verifica se há operadores ou comandos especiais
    tem_operador = any(token in operadores for token in tokens_para_analise)
    tem_comando_especial = any(token in comandos_especiais for token in tokens_para_analise)
    
    # Casos específicos que devem dar erro:
    if not tem_operador and not tem_comando_especial:
        numeros_e_vars = [t for t in tokens_para_analise if t.replace('.','').replace('-','').isdigit() or (t.isalpha() and t not in comandos_especiais)]
        
        # Se tem mais de 2 operandos, ou se tem parênteses duplos com 2 operandos sem operador
        if len(numeros_e_vars) > 2 or (len(numeros_e_vars) == 2 and linha.count('(') > 1):
            erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
            erro += f"    ERRO DE SINTAXE: Operandos sem operador - '{' '.join(numeros_e_vars)}' precisam de um operador"
            return False, erro
        
        # Verifica números/variáveis únicos em parênteses duplos (ex: ((5)))
        if len(numeros_e_vars) == 1 and linha.count('(') > 1:
            erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
            erro += f"    ERRO DE SINTAXE: Parênteses desnecessários - '{numeros_e_vars[0]}' não precisa de parênteses duplos"
            return False, erro
    
    # 6. Múltiplas expressões sem conexão
    if re.match(r'^\(\([^)]+\)\s*\([^)]+\)\)$', linha) and not any(cmd in linha for cmd in ['WHILE', 'FOR', 'IFELSE']):
        erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
        erro += f"    ERRO DE SINTAXE: Múltiplas expressões sem conexão - falta operador entre subexpressões"
        return False, erro
    
    # Padrão: ((expr1) (expr2) (expr3)) - três ou mais subexpressões sem lógica clara
    if re.match(r'^\(\([^)]+\)\s*\([^)]+\)\s*\([^)]+\)\)$', linha) and not any(cmd in linha for cmd in ['WHILE', 'FOR', 'IFELSE']):
        erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
        erro += f"    ERRO DE SINTAXE: Múltiplas expressões sem conexão - estrutura ambígua"
        return False, erro
    
    # Padrão: (((expr1)) ((expr2))) - parênteses excessivos
    if re.match(r'^\(\(\([^)]+\)\)\s*\(\([^)]+\)\)\)$', linha) and not any(cmd in linha for cmd in ['WHILE', 'FOR', 'IFELSE']):
        erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
        erro += f"    ERRO DE SINTAXE: Parênteses excessivos - estrutura mal formada"
        return False, erro
    
    # Se chegou até aqui, a validação básica passou
    return True, ""


def criarMensagemErro(linha: str, numero_linha: int, tipo_erro: str, detalhes: str = "") -> str:
    
    erro = f"Linha {numero_linha:02d}: Expressão '{linha}'\n"
    erro += f"    ERRO DE {tipo_erro}: {detalhes}"
    return erro