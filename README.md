# Analisador Sintático LL(1) - Fase 2

## Informações Institucionais

**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
**Disciplina:** Linguagens Formais e Autômatos
**Professor:** Frank Alcantara
**Ano:** 2025

### Integrantes do Grupo

- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

**Nome do grupo no Canvas:** RA2_1

---

## Descrição do Projeto

Analisador sintático descendente recursivo LL(1) para linguagem baseada em **notação polonesa reversa (RPN)**. O sistema integra o analisador léxico da Fase 1 com um parser sintático que constrói árvores de derivação e valida estruturas gramaticais.

### Características Principais

- Parser LL(1) com análise preditiva
- Suporte a expressões aritméticas, lógicas e relacionais em RPN
- Operadores: `+`, `-`, `*`, `/`, `|`, `%`, `^`, `>`, `<`, `>=`, `<=`, `==`, `!=`, `&&`, `||`, `!`
- Estruturas de controle: `FOR`, `WHILE`, `IFELSE`
- Comandos especiais: `RES` (histórico) e variáveis
- Geração de árvores sintáticas em formato ASCII
- Cálculo automático de conjuntos FIRST e FOLLOW
- Tabela de análise LL(1) construída dinamicamente

---

## Compilação e Execução

### Requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa

### Execução

```bash
python AnalisadorSintatico.py teste1.txt
python AnalisadorSintatico.py teste2.txt
python AnalisadorSintatico.py teste3.txt
```

### Arquivos de Saída

**`outputs/RA2/arvore_output.txt`** - Contém a árvore sintática em formato ASCII:

```
LINHA 1:
==================================================
PROGRAM
├── LINHA
│   ├── (
│   ├── CONTENT
│   │   ├── NUMERO_REAL
│   │   └── AFTER_NUM
│   │       ├── NUMERO_REAL
│   │       └── OPERATOR
│   │           └── +
│   └── )
└── PROGRAM_PRIME
    └── ε
```

---

## Estrutura do Projeto

```
RA2_1/
├── AnalisadorSintatico.py              # Programa principal - integra RA1 + RA2
├── teste1.txt                          # Arquivo de teste básico (na raiz)
├── teste2.txt                          # Arquivo de teste intermediário (na raiz)
├── teste3.txt                          # Arquivo de teste avançado (na raiz)
├── teste4_incorreto.txt                # Arquivo de teste com erros sintáticos
├── arvore_output.txt                   # Saída da última execução
├── grammar_documentation.md            # Documentação da gramática completa
├── LICENSE                             # Licença do projeto
├── README.md                           # Este arquivo
│
├── src/                                # Código-fonte
│   ├── RA1/                           # Fase 1 - Analisador Léxico
│   │   └── functions/
│   │       ├── python/                # Funções Python do analisador léxico
│   │       │   ├── __init__.py
│   │       │   ├── analisador_lexico.py    # Tokenização e análise léxica
│   │       │   ├── tokens.py               # Definições de tipos de tokens
│   │       │   ├── io_utils.py             # Utilitários de I/O
│   │       │   ├── rpn_calc.py             # Calculadora RPN
│   │       │   ├── validarExpressao.py     # Validação de expressões
│   │       │   └── exibirResultados.py     # Exibição de resultados
│   │       └── assembly/              # Geração de código Assembly RISC-V
│   │           ├── __init__.py
│   │           ├── builder.py              # Construtor principal
│   │           ├── header.py               # Cabeçalho assembly
│   │           ├── footer.py               # Rodapé assembly
│   │           ├── data_section.py         # Seção .data
│   │           ├── code_section.py         # Seção .text
│   │           ├── operations.py           # Operações aritméticas
│   │           ├── registers.py            # Gerenciamento de registradores
│   │           ├── routines.py             # Rotinas auxiliares
│   │           └── io.py                   # I/O assembly
│   │
│   └── RA2/                           # Fase 2 - Analisador Sintático LL(1)
│       └── functions/
│           └── python/                # Funções do parser LL(1)
│               ├── __init__.py
│               ├── lerTokens.py            # Leitura e processamento de tokens
│               ├── construirGramatica.py   # Construção da gramática LL(1)
│               ├── parsear.py              # Parser descendente recursivo
│               ├── gerarArvore.py          # Geração de árvore sintática
│               ├── configuracaoGramatica.py # Configuração da gramática
│               ├── calcularFirst.py        # Cálculo dos conjuntos FIRST
│               ├── calcularFollow.py       # Cálculo dos conjuntos FOLLOW
│               └── construirTabelaLL1.py   # Construção da tabela LL(1)
│
├── inputs/                             # Arquivos de entrada para testes
│   ├── RA1/                           # Entradas da Fase 1
│   │   ├── float/                     # Testes com ponto flutuante
│   │   │   ├── teste1.txt
│   │   │   ├── teste2.txt
│   │   │   ├── teste3.txt
│   │   │   └── teste_parenteses_completo.txt
│   │   └── int/                       # Testes para assembly (inteiros)
│   │       ├── teste1_assembly.txt
│   │       ├── teste2_assembly.txt
│   │       ├── teste3_assembly.txt
│   │       └── teste_parenteses_completo.txt
│   └── RA2/                           # Entradas da Fase 2
│       ├── teste1.txt                      # Operações básicas
│       ├── teste2.txt                      # Estruturas de controle
│       ├── teste3.txt                      # Casos complexos
│       └── teste4_incorreto.txt            # Casos com erros
│
├── outputs/                            # Arquivos de saída gerados
│   ├── RA1/                           # Saídas do analisador léxico
│   │   ├── tokens/
│   │   │   └── tokens_gerados.txt          # Tokens gerados
│   │   └── assembly/
│   │       ├── programa_completo.S         # Código assembly RISC-V
│   │       └── registers.inc               # Include de registradores
│   └── RA2/                           # Saídas do analisador sintático
│       └── arvore_output.txt               # Árvore sintática gerada
│
├── docs/                               # Documentação completa
│   ├── RA1/                           # Documentação da Fase 1
│   │   └── Github/
│   │       └── README.md                   # README original do RA1
│   └── RA2/                           # Documentação da Fase 2
│       ├── Github/
│       │   └── README.md                   # README específico do RA2
│       └── documents/                 # Documentação técnica detalhada
│           ├── 01_Grammar_Fundamentals.md
│           ├── 02_LL1_Parsing_and_Syntax_Analysis.md
│           ├── 03_FIRST_FOLLOW_Sets_Calculation.md
│           ├── 04_LL1_Table_Construction_and_Conflict_Resolution.md
│           ├── 05_Control_Structure_Syntax_Design.md
│           ├── 06_Complete_FIRST_FOLLOW_Calculation.md
│           ├── 07_LL1_Table_and_Conflict_Resolution.md
│           ├── 08_Grammar_Validation_and_Final_Specification.md
│           ├── grammar_analysis.md         # Análise completa da gramática
│           └── grammar_calculations.md     # Cálculos matemáticos detalhados
│
└── flowcharts/                         # Diagramas e fluxogramas
    ├── RA1/                           # Diagramas da Fase 1
    │   ├── Divisao_Inteira_e_Modulo.jpeg
    │   ├── Divisao_Real.jpeg
    │   ├── Multiplicacao_Inteira.jpeg
    │   ├── Multiplicacao_Real.jpeg
    │   ├── Potenciacao_Inteira_e_Real.jpeg
    │   ├── Soma_Inteira.jpeg
    │   ├── Soma_Real.jpeg
    │   ├── Subtracao_Inteira.jpeg
    │   └── Subtracao_Real.jpeg
    └── RA2/                           # Diagramas da Fase 2
        ├── RA2_Architecture_Overview.md    # Visão geral da arquitetura
        └── RA2_Function_Interfaces.md      # Interfaces entre funções
```

---

## Sintaxe da Linguagem

### Notação Polonesa Reversa (RPN)

A linguagem utiliza RPN, onde operadores aparecem após operandos:

```
(operando1 operando2 operador)
```

### Operadores Suportados

**Aritméticos:**
- `+` Adição
- `-` Subtração
- `*` Multiplicação
- `/` Divisão inteira
- `|` Divisão real
- `%` Resto (módulo)
- `^` Potenciação

**Comparação:**
- `>`, `<`, `>=`, `<=`, `==`, `!=`

**Lógicos:**
- `&&` AND
- `||` OR
- `!` NOT

### Exemplos

```
(3 4 +)                              → 7
((A B +) (C D *) /)                  → (A+B) / (C*D)
((5 3 >) (2 1 >) &&)                 → (5>3) AND (2>1)
(42 X)                               → armazena 42 em X
```

### Estruturas de Controle

**FOR - Laço de Repetição:**
```
(FOR (início)(fim)(incremento)(corpo))
```

**WHILE - Laço Condicional:**
```
(WHILE (condição)(corpo))
```

**IFELSE - Estrutura Condicional:**
```
(IFELSE (condição)(bloco_então)(bloco_senão))
```

---

## Funções Principais

### 1. `lerTokens(arquivo)`
Lê arquivo de tokens da Fase 1 e processa estruturas de controle.

### 2. `construirGramatica()`
Define gramática LL(1) completa e constrói tabelas de análise (FIRST, FOLLOW, tabela LL(1)).

### 3. `parsear(tokens, tabela_ll1)`
Parser descendente recursivo com detecção de erros sintáticos.

### 4. `gerarArvore(derivacao)`
Converte derivação em árvore sintática e salva em arquivo.

---

## Gramática LL(1)

### Status de Validação

✅ Sem conflitos FIRST/FIRST
✅ Sem conflitos FIRST/FOLLOW
✅ Sem recursão à esquerda
✅ Determinística com lookahead = 1
✅ Tabela LL(1) completa e sem ambiguidades

### Documentação Técnica Completa

Para visualizar a gramática completa, conjuntos FIRST/FOLLOW e tabela LL(1), consulte:

- **`docs/RA2/documents/grammar_analysis.md`** - Análise completa da gramática
- **`docs/RA2/documents/grammar_calculations.md`** - Demonstrações matemáticas detalhadas

---

## Tratamento de Erros

O analisador detecta e reporta:

- **Erros léxicos:** Tokens não reconhecidos, formato inválido
- **Erros sintáticos:** Token inesperado, estrutura gramatical inválida
- **Erros de estrutura:** Parênteses desbalanceados, expressões incompletas

**Exemplo de mensagem de erro:**
```
ERRO SINTÁTICO na linha 3:
Token encontrado: '+'
Token esperado: 'NUMERO_REAL', 'VARIAVEL', ou '('
Contexto: dentro de CONTENT
```

---

## Arquivos de Teste

### teste1.txt
Operações básicas, expressões simples, variáveis

### teste2.txt
Estruturas de controle, expressões aninhadas, operadores lógicos

### teste3.txt
Casos avançados, aninhamento profundo, casos de erro sintático

---

## Módulos do Código

### AnalisadorSintatico.py
Programa principal que coordena análise léxica (RA1) e sintática (RA2).

### src/RA2/configuracaoGramatica.py
Definição completa da gramática LL(1) em formato BNF/EBNF.

### src/RA2/first_follow.py
Cálculo de conjuntos NULLABLE, FIRST e FOLLOW com algoritmos de ponto fixo.

### src/RA2/parser.py
Motor do parser LL(1) com tabela de análise preditiva.

### src/RA2/arvore_sintatica.py
Estrutura de árvore sintática e visualização ASCII.

---

## Integração com RA1

O projeto reutiliza o analisador léxico da Fase 1:
- String/vetor de tokens como entrada
- Formato de tokens já definido
- Mesma lógica RPN e operadores
- Novos tokens para estruturas de controle
