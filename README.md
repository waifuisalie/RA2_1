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
├── src/                        # Código-fonte modular para RA2
│   └── RA1/                    # Código da Fase 1 (Analisador Léxico) para reuso
│       └── LFC---Analisador-Lexico/    # Projeto completo da Fase 1
│           ├── src/
│           │   ├── functions/
│           │   │   ├── analisador_lexico.py    # Analisador léxico original
│           │   │   ├── tokens.py               # Definições de tokens
│           │   │   ├── io_utils.py             # Utilitários de I/O
│           │   │   ├── rpn_calc.py             # Calculadora RPN
│           │   │   └── assembly/               # Geração de código assembly
│           │   └── main.py
│           └── README.md
├── flowcharts/                 # Documentação de arquitetura (existente)
│   ├── overview_flowchart.md
│   └── code_flowchart.md
└── github_issues_workflow.md   # Processo de colaboração da equipe (existente)
```

**Notas importantes:** 
- Conforme especificação do PDF, os arquivos de teste devem estar no mesmo diretório do código-fonte
- O diretório `src/RA1/` contém o código da Fase 1 (Analisador Léxico) como git submodule para reuso e integração
- Para clonar este repositório com o submodule: `git clone --recurse-submodules <repo-url>`

## Integração com a Fase 1 (RA1)

Este projeto (Fase 2) é construído sobre o código da Fase 1 (Analisador Léxico), que está localizado em `src/RA1/LFC---Analisador-Lexico/`. Conforme especificado no PDF, o analisador sintático LL(1) utiliza como entrada **o string/vetor de tokens gerado pelo analisador léxico da Fase 1**.

**Reutilização Específica da RA1:**
- **String de tokens:** Entrada principal do analisador sintático (conforme PDF: "Utilizar o string de tokens gerado por um analisador léxico, como o da Fase 1")
- **Formato de tokens:** Estrutura de dados já definida em `tokens.py`
- **Lógica RPN:** Mesmos operadores (+, -, *, |, /, %, ^) e comandos especiais ((N RES), (V MEM), (MEM))
- **Analisador léxico:** Base em `analisador_lexico.py` para geração de tokens

**Extensões Necessárias:**
- Novos tokens para estruturas de controle (loops e decisões)
- Tokens para operadores relacionais (>, <, ==, etc.)
- Integração da função `lerTokens(arquivo)` com o formato da Fase 1

**Nota sobre correções:** O PDF indica que "algumas questões relacionadas à geração e manipulação de tokens na Fase 1 podem precisar ser corrigidas durante o desenvolvimento da Fase 2".

### Trabalhando com o Submodule RA1

O código da Fase 1 está integrado como git submodule. Comandos úteis:

**Para clonar este repositório (novos membros do time):**
```bash
git clone --recurse-submodules https://github.com/seu-usuario/RA2_1.git
```

**Para atualizar RA1 com mudanças do repositório original:**
```bash
cd src/RA1/LFC---Analisador-Lexico
git pull origin main
cd ../../..
git add src/RA1/LFC---Analisador-Lexico
git commit -m "Update RA1 submodule to latest version"
```

**Se você já clonou sem submodules:**
```bash
git submodule update --init --recursive
```

**Para verificar o status do submodule:**
```bash
git submodule status
```

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
