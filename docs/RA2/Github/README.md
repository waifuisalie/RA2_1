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

## Compilação e Execução

```bash
# Executar o analisador sintático (arquivos de teste no mesmo diretório)
python AnalisadorSintatico.py teste1.txt
python AnalisadorSintatico.py teste2.txt  
python AnalisadorSintatico.py teste3.txt
```
===================================================================================
**Requisitos:**
- Python 3.8+
- Arquivo de tokens válido (gerado na Fase 1)
- Arquivos de teste no mesmo diretório do código-fonte (conforme especificação PDF)

## Estrutura do Projeto

```
RA2_1/
├── README.md                    # Este arquivo
├── AnalisadorSintatico.py      # Implementação principal (apenas a função main())
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
- o AnalisadorSintatico.py vai ter uma main() que vai incorporar o RA1 e RA2.
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

### Funções Principais Obrigatórias (Conforme PDF)

#### 1. `lerTokens(arquivo)` - **[Student 3 Responsibility]**
**Propósito**: Ler arquivo de tokens gerado na Fase 1 e processar estruturas de controle
- **Entrada**: Nome do arquivo contendo tokens da Fase 1
- **Funcionalidade**:
  - Carregar tokens no formato definido pelo grupo na Fase 1
  - Adicionar novos tokens para estruturas de controle (loops/decisões)
  - Incluir tokens para operadores relacionais (`>`, `<`, `==`, `!=`, etc.)
  - Implementar validação básica de tokens
  - Manter compatibilidade com formato RPN da Fase 1
- **Saída**: Vetor de tokens estruturado para uso no parser
- **Integração**: Fornece tokens processados para `parsear()`

#### 2. `construirGramatica()` - **[Student 1 Responsibility]**
**Propósito**: Definir gramática LL(1) completa e construir tabelas de análise
- **Entrada**: Nenhuma (gramática fixa definida pela equipe)
- **Funcionalidades Obrigatórias**:
  - Definir regras de produção para expressões RPN
  - Incluir regras para comandos especiais (`RES`, `MEM`)
  - Criar regras para estruturas de controle (decisão e laços)
  - Implementar `calcularFirst()` para todos os símbolos
  - Implementar `calcularFollow()` para não-terminais
  - Construir tabela LL(1) livre de conflitos via `construirTabelaLL1()`
  - Validar que gramática é determinística (sem ambiguidades)
- **Saída**: Estrutura contendo gramática, conjuntos FIRST/FOLLOW e tabela LL(1)
- **Documentação**: Gramática completa em EBNF (maiúsculas=não-terminais, minúsculas=terminais)

#### 3. `parsear(tokens, tabela_ll1)` - **[Student 2 Responsibility]**
**Propósito**: Parser descendente recursivo LL(1) com detecção de erros
- **Entrada**: Vetor de tokens + tabela LL(1) da função anterior
- **Implementação Obrigatória**:
  - Parser descendente recursivo usando tabela LL(1)
  - Buffer de entrada para controle de tokens
  - Pilha de análise para controle do parsing
  - Funções recursivas específicas para cada não-terminal
  - Sistema de detecção e recuperação de erros sintáticos
  - Geração de derivação durante processo de parsing
- **Validação**: Testar com expressões válidas/inválidas e estruturas de controle
- **Saída**: Estrutura de derivação ou erro sintático detalhado
- **Integração**: Fornece derivação para `gerarArvore()`

#### 4. `gerarArvore(derivacao)` - **[Student 4 Responsibility + Integration Lead]**
**Propósito**: Converter derivação em árvore sintática e coordenar integração
- **Entrada**: Estrutura de derivação gerada pelo parser
- **Funcionalidades**:
  - Transformar derivação em estrutura de árvore sintática
  - Implementar visualização em formato legível (texto/gráfico)
  - Salvar árvore em JSON ou formato customizado para fases futuras
  - Implementar função `main()` coordenando todas as etapas
  - Gerenciar interface de linha de comando
  - Criar funções de teste end-to-end do sistema completo
- **Saída**: Árvore sintática estruturada + arquivos de saída
- **Responsabilidade Extra**: Coordenar integração entre todos os módulos

### Funções Auxiliares Obrigatórias
- **`calcularFirst()`**: Calcular conjuntos FIRST para símbolos da gramática
- **`calcularFollow()`**: Calcular conjuntos FOLLOW para não-terminais
- **`construirTabelaLL1()`**: Construir tabela de parsing baseada em FIRST/FOLLOW
- **`validateGrammar()`**: Verificar se gramática é LL(1) sem conflitos

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

## Saída do Projeto RA2

### Entregáveis Principais:
1. **Árvore Sintática**: Gerada em formato JSON ou texto customizado, salva para uso nas fases futuras do compilador
2. **Documentação da Gramática**: Regras completas da gramática em formato EBNF com não-terminais em maiúsculas e terminais em minúsculas
3. **Conjuntos FIRST e FOLLOW**: Calculados e documentados para cada símbolo da gramática
4. **Tabela de Parsing LL(1)**: Tabela livre de conflitos mapeando pares (não-terminal, terminal) para regras de produção
5. **Documentação em Markdown**: Contém gramática, conjuntos, tabela e árvore sintática da última execução

### Estrutura dos Arquivos de Saída (Conforme Especificação PDF):
```
/RA2_1/
├── AnalisadorSintatico.py              # Analisador sintático principal (Python/C/C++)
├── teste1.txt, teste2.txt, teste3.txt  # Arquivos de teste obrigatórios (mín. 3, 10+ linhas)
├── README.md                           # Esta documentação completa
├── grammar_documentation.md            # Gramática EBNF, FIRST/FOLLOW, tabela LL(1), árvore sintática
└── syntax_tree_output.json             # Árvore sintática salva (JSON ou formato customizado)
```

## Requisitos de Entrega (Baseado no PDF)

### 1. Código-Fonte Obrigatório
- **Linguagem**: Python, C ou C++ (escolhido: Python)
- **Cabeçalho obrigatório**:
```python
# Integrantes do grupo (ordem alfabética):
# Breno Rossi Duarte - breno-rossi
# Francisco Bley Ruthes - fbleyruthes  
# Rafael Olivare Piveta - RafaPiveta
# Stefan Benjamim Seixas Lourenco Rodrigues - waifuisalie
#
# Nome do grupo no Canvas: RA2_1
```
- **Interface**: `python AnalisadorSintatico.py teste1.txt`
- **Todas as 4 funções principais** implementadas e funcionais

### 2. Arquivos de Teste Obrigatórios (Mínimo 3)
**Cada arquivo deve conter**:
- **Mínimo 10 linhas** de expressões por arquivo
- **Todas as operações aritméticas**: `+`, `-`, `*`, `|`, `/`, `%`, `^`
- **Comandos especiais**: `(N RES)`, `(V MEM)`, `(MEM)`
- **Pelo menos 1 laço de repetição** por arquivo
- **Pelo menos 1 tomada de decisão** por arquivo
- **Casos válidos e inválidos** para teste de erros sintáticos
- **Literais inteiros e reais** + uso de memórias (variáveis)
- **Expressões aninhadas** e casos extremos

### 3. Documentação Obrigatória
**README.md deve conter**:
- ✅ Informações institucionais (PUCPR, disciplina, professor)
- ✅ Integrantes em ordem alfabética
- ✅ Instruções de compilação/execução
- ✅ Documentação da sintaxe das estruturas de controle
- ✅ Exemplos de uso

**Arquivo Markdown separado deve incluir**:
- **Gramática completa** em formato EBNF
- **Conjuntos FIRST e FOLLOW** calculados
- **Tabela de Análise LL(1)** completa
- **Árvore sintática** da última execução representada

### 4. Repositório GitHub Obrigatório
- **Nome**: RA2_1 (conforme Canvas)
- **Visibilidade**: Público
- **Commits claros** com contribuições documentadas
- **Pull requests** registrando trabalho de cada membro
- **Issues** encorajadas para discussão de tarefas
- **Usuários fixos** (sem mudança durante desenvolvimento)

## Critérios de Avaliação (Conforme PDF)

### Funcionalidades do Analisador (70%)
**Penalidades Críticas**:
- ❌ **Cada operação aritmética não identificada**: -10%
- ❌ **Falha nos laços de repetição**: -20%
- ❌ **Falha na tomada de decisão**: -20%
- ❌ **Processar apenas números inteiros** (sem ponto flutuante): -50%
- ❌ **Falha na geração da árvore sintática**: -30%
- ❌ **Gramática não-LL(1) ou com conflitos**: -20%

### Organização e Legibilidade (15%)
**Requisitos**:
- ✅ Código claro, comentado e bem estruturado
- ✅ README.md completo com informações institucionais
- ✅ Instruções claras de compilação/execução
- ✅ Documentação da sintaxe das estruturas de controle
- ✅ Repositório GitHub organizado

### Robustez (15%)
**Requisitos**:
- ✅ Tratamento de erros em expressões complexas
- ✅ Mensagens de erro claras indicando linha e tipo
- ✅ Testes cobrindo casos válidos e inválidos
- ✅ Recuperação básica de erros sintáticos

### Prova de Autoria
- **Um aluno será sorteado** para explicar o projeto
- **Falha na explicação**: -35% da nota para todo o grupo
- **Todos os membros** devem entender o funcionamento completo
- **Qualquer pergunta** sobre qualquer parte do projeto deve ser respondida

## Requisitos Técnicos Específicos

### Gramática LL(1) Obrigatória
- **Sem conflitos**: Tabela determinística
- **Sem recursão à esquerda**: Todas eliminadas
- **Conjuntos FIRST/FOLLOW disjuntos**: Para cada produção
- **Não-ambígua**: Cada string tem exatamente uma análise válida
- **EBNF documentado**: Maiúsculas=não-terminais, minúsculas=terminais

### Precisão Numérica (Dependente da Arquitetura)
- **8 bits**: Meia precisão (16 bits, IEEE 754)
- **16 bits**: Precisão simples (32 bits, IEEE 754)  
- **32 bits**: Precisão dupla (64 bits, IEEE 754)
- **64 bits**: Precisão quádrupla (128 bits, IEEE 754)

### Integração Sequencial Obrigatória
1. **Passo 1**: Copiar `main()` e interface (Student 4)
2. **Passo 2**: Inserir `lerTokens()` + estruturas de controle (Student 3)
3. **Passo 3**: Adicionar `construirGramatica()` + tabela LL(1) (Student 1)
4. **Passo 4**: Incluir `parsear()` (Student 2)
5. **Passo 5**: Integrar `gerarArvore()` final (Student 4)

## Requisitos Adicionais Críticos (Baseados no PDF)

### Projeto "Aumentado por Inteligência Artificial"
**Permitido**:
- ✅ Gerar código repetitivo (boilerplate) e arquivos de configuração
- ✅ Explicar conceitos complexos e documentação
- ✅ Depurar mensagens de erro e sugerir correções
- ✅ Escrever testes unitários e documentação
- ✅ Otimizar e refatorar código existente
- ✅ Brainstorming de ideias de projetos e arquitetura

**PROIBIDO**:
- ❌ **Envio às Cegas**: Enviar código gerado por IA sem revisão/compreensão
- ❌ **Contornar Aprendizado**: Usar IA para completar objetivos centrais que você deve aprender
- ❌ **Violação de Licenças**: Código que viole políticas acadêmicas

**Princípio Fundamental**: "Você é o arquiteto e engenheiro; a IA é sua assistente. Você mantém total responsabilidade pelo código enviado."

### Avaliação Automatizada por IA
- Todos os trabalhos serão **pré-avaliados automaticamente** por ferramenta de IA
- Verificação de **originalidade do texto e autoria do código**
- Cumprimento de **todas as regras de entrega e desenvolvimento**
- Resultado da avaliação automatizada = **nota base do trabalho**
- Nota pode ser alterada na **prova de autoria**

### Regras de Escopo Específicas
- **Cada arquivo de texto** representa um escopo de memória independente
- **MEM** pode ser qualquer conjunto de letras maiúsculas (ex: `MEM`, `VAR`, `X`, `CONTADOR`)
- **RES** é uma keyword fixa da linguagem
- **Memória não inicializada** retorna 0 por padrão

### Expressões Aninhadas (Sem Limite)
Exemplos obrigatórios para teste:
```
(A (C D *) +)           # Soma A ao produto de C e D
((A B %) (D E *) /)     # Divide resto de A por B pelo produto de D e E
((A B +) (C D *) |)     # Divisão real da soma de A e B pelo produto de C e D
```

### Funções de Teste Específicas (PDF Seção 3.5)
**Obrigatório implementar**:
- Funções de teste específicas para validar o analisador sintático
- **Cobertura obrigatória**:
  - Expressões válidas simples e aninhadas
  - Estruturas de controle válidas  
  - Entradas inválidas (erros sintáticos)
  - Casos extremos (aninhamento profundo, expressões vazias)

### Operações Exclusivas com Inteiros
- **Divisão inteira** (`/`) e **resto** (`%`) são realizadas **exclusivamente com números inteiros**
- Todas as outras operações suportam ponto flutuante

### Arquivos no Mesmo Diretório (CRÍTICO)
- **Arquivos de teste devem estar no mesmo diretório do código-fonte**
- Processamento via argumento de linha de comando: `./AnalisadorSintatico teste1.txt`
- **NÃO** em subdiretórios separados

### Casos de Teste com Erros Sintáticos (Obrigatório)
Cada arquivo de teste deve incluir:
- **Casos válidos** para validar funcionalidade
- **Casos inválidos** para validar tratamento de erros
- Exemplos: `(A B + C)` (erro), parênteses não balanceados, operadores inválidos

### Warnings Importantes do PDF
- ⚠️ **Plágio resultará na anulação do trabalho**
- ⚠️ **Trabalhos identificados como cópias terão nota zerada**
- ⚠️ **Grupos com mais de 4 membros terão trabalho anulado**
- ⚠️ **Aluno não pode trocar usuário GitHub durante desenvolvimento**
- ⚠️ **Repositório não pode ser alterado para privado**

### Diferença de Saída entre RA1 e RA2:
```
RA1 Saída: Tokens + Resultados RPN + Código Assembly + Relatórios de execução
RA2 Saída: Árvore Sintática + Documentação de gramática + Validação sintática (sem execução)
```

## Novos Tokens e Estruturas de Controle

### Propósito dos Novos Tokens:
Os novos tokens de estruturas de controle servem **apenas para propósitos de parsing sintático**:

- **Definição de Sintaxe**: Definem tipos de tokens para loops e decisões (ex: `FOR`, `WHILE`, `IF`, `ELSE`)
- **Regras Gramaticais**: Criam regras de produção para estruturas de controle em notação RPN pós-fixa
- **Integração na Árvore**: Incluem estruturas de controle na geração da árvore sintática
- **Validação Sintática**: Garantem que estruturas de controle sigam padrões gramaticais corretos

### O que os Novos Tokens Significam:
- **NÃO para execução**: Tokens não implementam lógica real de loop ou condicional
- **Apenas estrutura**: Definem como estruturas de controle devem ser sintaticamente organizadas
- **Conformidade gramatical**: Garantem que estruturas mantenham padrão RPN pós-fixa entre parênteses
- **Preparação futura**: Fornecem base para análise semântica e geração de código em fases posteriores

### Exemplo de Validação Sintática:
```
✅ Válido:   (1 10 I FOR)           # Loop de 1 a 10 com contador I
✅ Válido:   (A B > IF X ELSE Y)    # Se A > B então X senão Y
❌ Inválido: (FOR 1 10 I)           # Ordem errada - FOR deve ser pós-fixa
❌ Inválido: (A B IF)               # Faltando cláusula ELSE
❌ Inválido: A B > IF X ELSE Y      # Faltando parênteses
```

### O que Significa "Seguir a Gramática Corretamente":

Validação gramatical significa que as estruturas de controle devem corresponder às **regras de sintaxe** definidas. As regras gramaticais especificam **padrões válidos** para como os tokens podem ser organizados.

#### Definição de Regras Gramaticais:
```python
# Exemplo de regras gramaticais que você pode criar:
LOOP → '(' EXPR EXPR IDENTIFIER 'FOR' ')'
DECISION → '(' EXPR EXPR 'IF' STATEMENT 'ELSE' STATEMENT ')'
EXPR → NUMBER | IDENTIFIER | '(' EXPR EXPR OPERATOR ')'
```

#### Exemplos de Sintaxe Válida vs Inválida:

**✅ Sintaxe Válida (segue a gramática):**
```
(1 10 I FOR)           # Loop de 1 a 10 com contador I
(A B > IF X ELSE Y)    # Se A > B então X senão Y  
((A B +) 5 * Z MEM)    # Armazenar (A+B)*5 na memória Z
```

**❌ Sintaxe Inválida (quebra a gramática):**
```
(FOR 1 10 I)           # Ordem errada - FOR deve estar no final (pós-fixa)
(A B IF)               # Faltando cláusula ELSE
(1 10 FOR)             # Faltando variável contador
A B > IF X ELSE Y      # Faltando parênteses obrigatórios
```

### Processo de Validação Gramatical:

O parser deve:
1. **Aceitar estruturas válidas** - Analisá-las na árvore sintática
2. **Rejeitar estruturas inválidas** - Reportar erros sintáticos específicos

#### Exemplo do Processo de Validação:
```python
# Exemplo simplificado de verificação gramatical
def parse_loop(tokens):
    if tokens[0] != '(':
        return SyntaxError("Esperado '(' no início")
    if tokens[-2] != 'FOR':
        return SyntaxError("Esperada palavra-chave 'FOR' em posição pós-fixa") 
    if tokens[-1] != ')':
        return SyntaxError("Esperado ')' no final")
    if len(tokens) < 5:
        return SyntaxError("Loop incompleto: esperados limite_inicial, limite_final, contador, FOR")
    # Mais regras de validação...
    return build_syntax_tree_node(tokens)

# Exemplo de uso:
tokens = ['(', '1', '10', 'I', 'FOR', ')']  # Válido
result = parse_loop(tokens)  # ✅ Constrói nó da árvore sintática

tokens = ['(', 'FOR', '1', '10', 'I', ')']  # Inválido  
result = parse_loop(tokens)  # ❌ Retorna SyntaxError
```

#### Tipos de Erros Sintáticos Reportados:
- `"Erro: Esperada variável contador após limites do loop"`
- `"Erro: Faltando cláusula ELSE no comando IF"`
- `"Erro: Palavra-chave FOR deve estar em posição pós-fixa"`
- `"Erro: Parênteses não balanceados na expressão"`
- `"Erro: Operador inválido em expressão RPN"`

**Conceito-chave**: Você está definindo as "sentenças legais" na sua linguagem de programação e garantindo que a entrada siga essas regras.

## Integração Futura

A árvore sintática gerada pela RA2 será utilizada nas fases subsequentes do compilador para:
- **Análise Semântica**: Verificação de tipos e resolução de escopo
- **Geração de Código**: Conversão da árvore sintática para código alvo
- **Otimização**: Melhoria da eficiência do código gerado
- **Saída Final Assembly**: Pipeline completo de compilação
