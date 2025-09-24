# RA2_1 - Analisador Sintático LL(1)

**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)  
**Disciplina:** Linguagens Formais e Autômatos  
**Projeto:** Fase 2 - Analisador Sintático LL(1) para RPN

## Integrantes do Grupo (ordem alfabética)
- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

**Nome do grupo no Canvas:** RA2_1

## Descrição do Projeto

Este projeto implementa um analisador sintático LL(1) para uma linguagem simplificada baseada em Notação Polonesa Reversa (RPN). O sistema processa tokens gerados na Fase 1 e constrói uma árvore sintática validando a sintaxe segundo uma gramática LL(1) livre de conflitos.

## Compilação e Execução

```bash
# Executar o analisador sintático (arquivos de teste no mesmo diretório)
python AnalisadorSintatico.py teste1.txt
python AnalisadorSintatico.py teste2.txt  
python AnalisadorSintatico.py teste3.txt
```

**Requisitos:**
- Python 3.8+
- Arquivo de tokens válido (gerado na Fase 1)
- Arquivos de teste no mesmo diretório do código-fonte (conforme especificação PDF)

## Estrutura do Projeto

```
RA2_1/
├── README.md                    # Este arquivo
├── AnalisadorSintatico.py      # Implementação principal (todas as 4 funções)
├── teste1.txt                  # Arquivo de teste 1 (operações básicas)
├── teste2.txt                  # Arquivo de teste 2 (estruturas de controle)  
├── teste3.txt                  # Arquivo de teste 3 (casos complexos/inválidos)
├── grammar_documentation.md    # Gramática EBNF, conjuntos FIRST/FOLLOW, tabela LL(1), árvore sintática
├── flowcharts/                 # Documentação de arquitetura (existente)
│   ├── overview_flowchart.md
│   └── code_flowchart.md
└── github_issues_workflow.md   # Processo de colaboração da equipe (existente)
```

**Nota importante:** Conforme especificação do PDF, os arquivos de teste devem estar no mesmo diretório do código-fonte, não em subdiretórios.

## Funcionalidades Implementadas

### Funções Principais
- `lerTokens(arquivo)` - Leitura e processamento de tokens
- `construirGramatica()` - Construção da gramática LL(1) e tabelas
- `parsear(tokens, tabela_ll1)` - Análise sintática com LL(1)
- `gerarArvore(derivacao)` - Geração da árvore sintática

### Operadores Suportados
- Aritméticos: `+`, `-`, `*`, `|` (divisão real), `/` (divisão inteira), `%` (módulo), `^` (potência)
- Comandos especiais: `(N RES)`, `(V MEM)`, `(MEM)`
- Estruturas de controle: Loops e decisões (sintaxe será documentada)

## Formato RPN

```
(A B op)        # Operação binária: A operador B
(N RES)         # Resultado de N linhas anteriores
(V MEM)         # Armazenar valor V na memória
(MEM)           # Recuperar valor da memória
```

## Arquivos de Saída

- **Árvore sintática:** JSON ou formato texto customizado
- **Documentação da gramática:** Regras EBNF, conjuntos FIRST/FOLLOW, tabela LL(1)
- **Relatório de análise:** Resultado da última execução
