# RA2_1 - Analisador Sintático LL(1)

**Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)  
**Disciplina:** Linguagens Formais e Autômatos  
**Professor:** Frank Alcantara
**Projeto:** Fase 2 - Analisador Sintático LL(1) para RPN

## Integrantes do Grupo (ordem alfabética)
- Breno Rossi Duarte - breno-rossi
- Francisco Bley Ruthes - fbleyruthes
- Rafael Olivare Piveta - RafaPiveta
- Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie

**Nome do grupo no Canvas:** RA2_1

## Descrição do Projeto

Este projeto implementa um analisador sintático LL(1) para uma linguagem simplificada baseada em Notação Polonesa Reversa (RPN). O sistema processa tokens gerados na Fase 1 e constrói uma árvore sintática validando a sintaxe segundo uma gramática LL(1) livre de conflitos.

## Requisitos e Dependências

- **Python**: 3.7 ou superior
- **Módulos**: Todos os módulos são internos ao projeto (sem dependências externas)
- **Estrutura**: Manter a estrutura de diretórios `src/RA1/` e `src/RA2/`

## Compilação e Execução

```bash
# Executar o analisador sintático (arquivos de teste no mesmo diretório)
python AnalisadorSintatico.py teste1.txt
python AnalisadorSintatico.py teste2.txt
python AnalisadorSintatico.py teste3.txt
```

### Saída do Programa
- **Console**: Resultado da análise sintática e árvore de derivação
- **Arquivo**: `outputs/RA2/arvore_output.txt` - Árvore sintática em formato ASCII

## Depuração

### Tipos de Erro
- **Erro Léxico**: Token não reconhecido ou malformado
- **Erro Sintático**: Estrutura não conforme à gramática LL(1)
- **Erro de Arquivo**: Arquivo de teste não encontrado

### Dicas de Depuração
1. **Verificar parênteses**: Toda expressão deve estar entre `(` e `)`
2. **Conferir operadores**: Use operadores suportados: `+`, `-`, `*`, `/`, `%`, `^`, `>`, `<`, `>=`, `<=`, `==`, `!=`, `&&`, `||`, `!`
3. **Validar sintaxe RPN**: Operandos antes dos operadores: `(3 4 +)`
4. **Testar estruturas**: Use keywords corretas: `FOR`, `WHILE`, `IFELSE`

## Características da Linguagem

### Operadores Aritméticos
- **Adição**: `(3 4 +)` → 7
- **Subtração**: `(10 4 -)` → 6
- **Multiplicação**: `(2 3 *)` → 6
- **Divisão**: `(9 2 /)` → 4.5
- **Módulo**: `(10 3 %)` → 1
- **Potência**: `(2 3 ^)` → 8

### Operadores de Comparação
- **Maior**: `(5 3 >)` → verdadeiro
- **Menor**: `(3 5 <)` → verdadeiro
- **Maior ou igual**: `(5 5 >=)` → verdadeiro
- **Menor ou igual**: `(3 5 <=)` → verdadeiro
- **Igual**: `(5 5 ==)` → verdadeiro
- **Diferente**: `(5 3 !=)` → verdadeiro

### Operadores Lógicos
- **E lógico**: `((A 5 >) (B 0 >) &&)` → verdadeiro se A > 5 AND B > 0
- **OU lógico**: `((A 0 ==) (B 0 ==) ||)` → verdadeiro se A == 0 OR B == 0
- **NÃO lógico**: `((A 5 >) !)` → verdadeiro se NOT (A > 5)

### Comandos Especiais
- **Armazenamento**: `(42 X)` → armazena 42 na variável X
- **Recuperação**: `(X)` → recupera valor armazenado em X
- **Histórico**: `(5 RES)` → resultado de 5 operações anteriores

### Expressões Aninhadas
```
((A B +) (C D *) /)        # (A+B) / (C*D)
(((X Y *) Z +) W -)        # ((X*Y) + Z) - W
((3 4 +) (5 6 *) >)        # (3+4) > (5*6)
```

## Estruturas de Controle

### Estrutura FOR
**Sintaxe**: `(FOR (início)(fim)(incremento)(corpo))`

**Exemplo**:
```
(FOR (1)(10)(2)(((P 1 +) P)((P 2 *) Q)))
```
- Inicia P=1, vai até 10, incremento de 2
- Corpo: P = P + 1, Q = P * 2

### Estrutura WHILE
**Sintaxe**: `(WHILE (condição)(corpo))`

**Exemplo**:
```
(WHILE (X 5 <)(((X 1 +) X)((X 2 *) Y)))
```
- Enquanto X < 5
- Corpo: X = X + 1, Y = X * 2

### Estrutura IF-ELSE
**Sintaxe**: `(IFELSE (condição)(bloco_então)(bloco_senão))`

**Exemplos**:
```
(IFELSE ((A B >) (C D <=) &&)(1)(0))
```
- Se (A > B) AND (C <= D), então 1, senão 0

```
(IFELSE (M 0 >)((M N))((0 N)))
```
- Se M > 0, então N = M, senão N = 0

### Precedência e Aninhamento
- Estruturas podem ser aninhadas sem limite
- Parênteses determinam precedência
- Avaliação segue ordem postfixa (RPN)

## Arquitetura do Analisador Sintático LL(1)

### Funções Principais (RA2)

#### **`construirGramatica()`**
- **Responsabilidade**: Constrói a estrutura completa da gramática LL(1)
- **Funcionalidade**:
  - Define regras de produção para RPN, comandos especiais e estruturas de controle
  - Calcula conjuntos FIRST e FOLLOW automaticamente
  - Gera tabela de análise LL(1) livre de conflitos
  - Valida que a gramática é LL(1) sem ambiguidades
- **Retorna**: Estrutura de dados com gramática, FIRST, FOLLOW e tabela LL(1)

#### **`lerTokens(arquivo)`**
- **Responsabilidade**: Lê e valida tokens do arquivo de entrada
- **Funcionalidade**:
  - Processa arquivos de teste linha por linha
  - Reconhece tokens da Fase 1 (números, operadores básicos)
  - Adiciona tokens RA2 (FOR, WHILE, IFELSE, operadores relacionais/lógicos)
  - Valida sintaxe básica e estrutura de parênteses
- **Retorna**: Lista de tokens estruturados para análise sintática

#### **`gerarArvore(derivacao)`**
- **Responsabilidade**: Converte derivação do parser em árvore sintática
- **Funcionalidade**:
  - Transforma sequência de derivações em estrutura de árvore
  - Gera representação ASCII para visualização
  - Salva resultado em `outputs/RA2/arvore_output.txt`
  - Suporta aninhamento complexo de estruturas de controle
- **Retorna**: Árvore sintática em formato texto

### Funções de Análise Gramática

#### **`calcularFirst()`**
- **Funcionalidade**: Calcula conjuntos FIRST para todos os símbolos da gramática
- **Algoritmo**: Implementa algoritmo clássico de FIRST com mapeamento de tokens reais
- **Uso**: Base para construção da tabela LL(1)

#### **`calcularFollow()`**
- **Funcionalidade**: Calcula conjuntos FOLLOW para não-terminais
- **Dependência**: Utiliza conjuntos FIRST previamente calculados
- **Uso**: Completa informações necessárias para tabela LL(1)

#### **`construirTabelaLL1()`**
- **Funcionalidade**: Constrói tabela de análise LL(1) livre de conflitos
- **Validação**: Detecta e reporta conflitos FIRST/FIRST e FIRST/FOLLOW
- **Resultado**: Tabela determinística para parsing

#### **`configuracaoGramatica.py`**
- **Conteúdo**: Gramática LL(1) corrigida com padrão de continuação
- **Inovação**: Usa não-terminais intermediários (AFTER_VAR_OP) para eliminar conflitos
- **Status**: Matematicamente provada como LL(1) compliant

### Estrutura de Classes

#### **`NoArvore`**
- **Funcionalidade**: Representa nós da árvore sintática
- **Métodos**:
  - `adicionar_filho()`: Adiciona nós filhos
  - `desenhar_ascii()`: Gera representação visual ASCII
- **Uso**: Construção de árvores sintáticas hierárquicas

### Integração das Funções
1. **lerTokens()** → processa arquivo de entrada
2. **construirGramatica()** → prepara estruturas de análise
3. **Parser interno** → realiza análise sintática descendente
4. **gerarArvore()** → produz árvore sintática final

## Especificação Técnica da Gramática LL(1)

### Regras de Produção (EBNF)

```ebnf
PROGRAM → LINHA PROGRAM_PRIME
PROGRAM_PRIME → LINHA PROGRAM_PRIME | ε
LINHA → ABRE_PARENTESES CONTENT FECHA_PARENTESES

CONTENT → NUMERO_REAL AFTER_NUM
        | VARIAVEL AFTER_VAR
        | ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR
        | FOR FOR_STRUCT
        | WHILE WHILE_STRUCT
        | IFELSE IFELSE_STRUCT

AFTER_NUM → NUMERO_REAL OPERATOR
         | VARIAVEL AFTER_VAR_OP
         | ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR
         | RES

AFTER_VAR_OP → OPERATOR | ε

AFTER_VAR → NUMERO_REAL OPERATOR
         | VARIAVEL OPERATOR
         | ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR
         | ε

AFTER_EXPR → NUMERO_REAL OPERATOR
          | VARIAVEL OPERATOR
          | ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR

EXPR → NUMERO_REAL AFTER_NUM
     | VARIAVEL AFTER_VAR
     | ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR

OPERATOR → ARITH_OP | COMP_OP | LOGIC_OP
ARITH_OP → SOMA | SUBTRACAO | MULTIPLICACAO | DIVISAO | RESTO | POTENCIA
COMP_OP → MENOR | MAIOR | IGUAL | MENOR_IGUAL | MAIOR_IGUAL | DIFERENTE
LOGIC_OP → AND | OR | NOT

FOR_STRUCT → NUMERO_REAL NUMERO_REAL VARIAVEL LINHA
WHILE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA
IFELSE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA LINHA
```

### Símbolos da Gramática

#### Símbolos Terminais
```
NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, FECHA_PARENTESES, RES
FOR, WHILE, IFELSE
SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO, RESTO, POTENCIA
MENOR, MAIOR, MENOR_IGUAL, MAIOR_IGUAL, IGUAL, DIFERENTE
AND, OR, NOT, FIM
```

#### Símbolos Não-Terminais
```
PROGRAM, PROGRAM_PRIME, LINHA, CONTENT
AFTER_NUM, AFTER_VAR_OP, AFTER_VAR, AFTER_EXPR, EXPR
OPERATOR, ARITH_OP, COMP_OP, LOGIC_OP
FOR_STRUCT, WHILE_STRUCT, IFELSE_STRUCT
```

### Conjuntos FIRST

```
FIRST(PROGRAM) = {ABRE_PARENTESES}
FIRST(PROGRAM_PRIME) = {ABRE_PARENTESES, ε}
FIRST(LINHA) = {ABRE_PARENTESES}
FIRST(CONTENT) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, FOR, WHILE, IFELSE}
FIRST(AFTER_NUM) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, RES}
FIRST(AFTER_VAR_OP) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO, RESTO, POTENCIA,
                       MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE,
                       AND, OR, NOT, ε}
FIRST(AFTER_VAR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, ε}
FIRST(AFTER_EXPR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES}
FIRST(EXPR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES}
FIRST(OPERATOR) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO, RESTO, POTENCIA,
                  MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE,
                  AND, OR, NOT}
FIRST(ARITH_OP) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO, RESTO, POTENCIA}
FIRST(COMP_OP) = {MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE}
FIRST(LOGIC_OP) = {AND, OR, NOT}
FIRST(FOR_STRUCT) = {NUMERO_REAL}
FIRST(WHILE_STRUCT) = {ABRE_PARENTESES}
FIRST(IFELSE_STRUCT) = {ABRE_PARENTESES}
```

### Conjuntos FOLLOW

```
FOLLOW(PROGRAM) = {FIM}
FOLLOW(PROGRAM_PRIME) = {FIM}
FOLLOW(LINHA) = {ABRE_PARENTESES, FIM}
FOLLOW(CONTENT) = {FECHA_PARENTESES}
FOLLOW(AFTER_NUM) = {FECHA_PARENTESES}
FOLLOW(AFTER_VAR_OP) = {FECHA_PARENTESES}
FOLLOW(AFTER_VAR) = {FECHA_PARENTESES}
FOLLOW(AFTER_EXPR) = {FECHA_PARENTESES}
FOLLOW(EXPR) = {FECHA_PARENTESES}
FOLLOW(OPERATOR) = {FECHA_PARENTESES}
FOLLOW(ARITH_OP) = {FECHA_PARENTESES}
FOLLOW(COMP_OP) = {FECHA_PARENTESES}
FOLLOW(LOGIC_OP) = {FECHA_PARENTESES}
FOLLOW(FOR_STRUCT) = {FECHA_PARENTESES}
FOLLOW(WHILE_STRUCT) = {FECHA_PARENTESES}
FOLLOW(IFELSE_STRUCT) = {FECHA_PARENTESES}
```

### Tabela de Análise LL(1)

| Non-Terminal | ( | ) | NUM | VAR | FOR | WHILE | IFELSE | RES | OPERATORS | $ |
|-------------|---|---|-----|-----|-----|-------|--------|-----|-----------|---|
| PROGRAM | 1 | - | - | - | - | - | - | - | - | - |
| PROGRAM_PRIME | 2 | - | - | - | - | - | - | - | - | 3 |
| LINHA | 4 | - | - | - | - | - | - | - | - | - |
| CONTENT | 7 | - | 5 | 6 | 8 | 9 | 10 | - | - | - |
| AFTER_NUM | 13 | - | 11 | 12 | - | - | - | 14 | - | - |
| AFTER_VAR_OP | - | 16 | - | - | - | - | - | - | 15 | - |
| AFTER_VAR | 19 | 20 | 17 | 18 | - | - | - | - | - | - |
| AFTER_EXPR | 23 | - | 21 | 22 | - | - | - | - | - | - |
| EXPR | 26 | - | 24 | 25 | - | - | - | - | - | - |
| OPERATOR | - | - | - | - | - | - | - | - | 27,28,29 | - |
| FOR_STRUCT | - | - | 45 | - | - | - | - | - | - | - |
| WHILE_STRUCT | 46 | - | - | - | - | - | - | - | - | - |
| IFELSE_STRUCT | 47 | - | - | - | - | - | - | - | - | - |

**Legenda**: NUM=NUMERO_REAL, VAR=VARIAVEL, OPERATORS=todos os operadores

### Validação LL(1) - Status

✅ **Sem conflitos FIRST/FIRST**: Todas as produções têm conjuntos FIRST disjuntos
✅ **Sem conflitos FIRST/FOLLOW**: Produções ε satisfazem condições LL(1)
✅ **Sem recursão à esquerda**: Apenas recursão à direita
✅ **Determinística**: Decisão com lookahead = 1
✅ **Tabela completa**: Cada célula contém no máximo uma produção

**Resultado**: Gramática matematicamente validada como LL(1) compliant
