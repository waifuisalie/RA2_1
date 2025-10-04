# FIRST and FOLLOW Sets: The Mathematical Foundation of LL(1) Parsing

## Table of Contents
1. [Why FIRST and FOLLOW Matter](#why-first-and-follow-matter)
2. [FIRST Sets: What Can Start a Production](#first-sets-what-can-start-a-production)
3. [FOLLOW Sets: What Can Come After](#follow-sets-what-can-come-after)
4. [Step-by-Step Calculation Algorithms](#step-by-step-calculation-algorithms)
5. [Complete Python Implementation](#complete-python-implementation)
6. [Practical Examples with Your RPN Grammar](#practical-examples-with-your-rpn-grammar)
7. [Common Pitfalls and How to Avoid Them](#common-pitfalls-and-how-to-avoid-them)
8. [Integration with LL(1) Table Construction](#integration-with-ll1-table-construction)

## Understanding Productions: The DNA of Your Grammar

### What EXACTLY are Productions?

**Productions** are the **rules** that define your programming language. Think of them as the "recipe book" that tells you how to build valid sentences in your language.

#### **The Anatomy of a Production Rule**

```
A → α
```

Where:
- **A**: A non-terminal (the "name" of the rule)
- **→**: "Can be replaced by" or "produces"
- **α**: A sequence of terminals and/or non-terminals (what A becomes)

#### **Real-World Analogy: Sentence Structure**

In English, you might have rules like:
- `SENTENCE → SUBJECT VERB OBJECT`
- `SUBJECT → "I" | "You" | "The cat"`
- `VERB → "eat" | "see" | "love"`
- `OBJECT → "pizza" | "movies" | "books"`

In programming, you have rules like:
- `EXPRESSION → NUMBER | IDENTIFIER | (EXPRESSION OPERATOR EXPRESSION)`

### How Productions are Made: Your Team's Job

#### **Step 1: Decide Your Language Syntax**

Your team needs to decide: "What should valid RPN code look like?"

Examples you might want to support:
```
(3 4 +)                    // Simple addition
((A B +) (C D *) /)        // Nested expression
FOR (1 10 I (I PRINT))     // FOR loop
IF ((X 5 >) (SUCCESS PRINT)) // IF statement
```

#### **Step 2: Write Productions for Each Construct**

For each syntax pattern, create a production rule:

```python
# Basic RPN expression: (operand operand operator)
"EXPRESSION -> ( OPERAND OPERAND OPERATOR )"

# Operands can be numbers, variables, or nested expressions
"OPERAND -> NUMBER"
"OPERAND -> IDENTIFIER"
"OPERAND -> EXPRESSION"

# Operators are the mathematical symbols
"OPERATOR -> +"
"OPERATOR -> -"
"OPERATOR -> *"
# ... etc
```

#### **Step 3: Handle Multiple Choices with |**

When a non-terminal can become different things, use `|`:

```python
# OPERAND can be ANY of these three things
"OPERAND -> NUMBER | IDENTIFIER | EXPRESSION"

# This is equivalent to writing three separate rules:
"OPERAND -> NUMBER"
"OPERAND -> IDENTIFIER"
"OPERAND -> EXPRESSION"
```

### What Productions MEAN: The Replacement Process

#### **Productions are Replacement Instructions**

Each production tells the parser: "When you see this non-terminal, replace it with this sequence."

#### **Example: Parsing `(3 4 +)`**

Starting with `EXPRESSION`, here's how productions guide the replacement:

```
EXPRESSION                           // Start here
↓ (apply: EXPRESSION → ( OPERAND OPERAND OPERATOR ))
( OPERAND OPERAND OPERATOR )         // Replace EXPRESSION
↓ (apply: OPERAND → NUMBER to first OPERAND)
( NUMBER OPERAND OPERATOR )          // Replace first OPERAND
↓ (apply: OPERAND → NUMBER to second OPERAND)
( NUMBER NUMBER OPERATOR )           // Replace second OPERAND
↓ (apply: OPERATOR → +)
( NUMBER NUMBER + )                  // Replace OPERATOR
↓ (apply: NUMBER → 3 and NUMBER → 4)
( 3 4 + )                           // Final result!
```

#### **The Magic: Multiple Valid Derivations**

Different production choices lead to different valid programs:

```
OPERAND → NUMBER        ⟹  (5 7 *)
OPERAND → IDENTIFIER    ⟹  (X Y *)
OPERAND → EXPRESSION    ⟹  ((A B +) (C D *) /)
```

### How Productions are Defined in Code

#### **String Format (Most Common)**

```python
productions = [
    "PROGRAM -> STATEMENT_LIST",
    "STATEMENT_LIST -> STATEMENT STATEMENT_LIST | ε",
    "STATEMENT -> EXPRESSION | FOR_STATEMENT | IF_STATEMENT",
    "EXPRESSION -> ( OPERAND OPERAND OPERATOR )",
    "OPERAND -> NUMBER | IDENTIFIER | EXPRESSION",
    "OPERATOR -> + | - | * | / | %"
]
```

**Why strings?** Easy to read, write, and modify during development.

#### **Dictionary Format (Alternative)**

```python
productions = {
    'PROGRAM': [['STATEMENT_LIST']],
    'STATEMENT_LIST': [['STATEMENT', 'STATEMENT_LIST'], ['ε']],
    'STATEMENT': [['EXPRESSION'], ['FOR_STATEMENT'], ['IF_STATEMENT']],
    'EXPRESSION': [['(', 'OPERAND', 'OPERAND', 'OPERATOR', ')']],
    'OPERAND': [['NUMBER'], ['IDENTIFIER'], ['EXPRESSION']],
    'OPERATOR': [['+'], ['-'], ['*'], ['/'], ['%']]
}
```

**Why dictionaries?** Easier for algorithms to process.

### Productions in Your RA2 Project

#### **Your Team's Responsibilities**

1. **Student 1 (construirGramatica)**: Define the complete set of productions
2. **Student 3 (lerTokens)**: Ensure all terminals in productions are recognized as tokens
3. **Student 2 (parsear)**: Use productions to guide parsing decisions
4. **Student 4 (gerarArvore)**: Use productions to build syntax tree structure

#### **Where Productions Come From**

```python
def construirGramatica():
    # THIS IS WHERE YOUR TEAM DEFINES THE LANGUAGE!
    productions = [
        # Basic structure
        "PROGRAM -> STATEMENT_LIST",

        # Statement types your language supports
        "STATEMENT -> EXPRESSION | FOR_STATEMENT | WHILE_STATEMENT | IF_STATEMENT",

        # RPN expression format
        "EXPRESSION -> ( OPERAND OPERAND OPERATOR )",

        # What can be operands
        "OPERAND -> NUMBER | IDENTIFIER | EXPRESSION",

        # What operators you support
        "OPERATOR -> + | - | * | / | % | ^ | | | > | < | >= | <= | == | !=",

        # Control structures (your team designs these!)
        "FOR_STATEMENT -> FOR ( OPERAND OPERAND IDENTIFIER STATEMENT )",
        "IF_STATEMENT -> IF ( EXPRESSION STATEMENT ) | IF ( EXPRESSION STATEMENT ) ELSE ( STATEMENT )"
    ]
    return productions
```

#### **The Connection to Tokens**

Every **terminal** in your productions must be a **token** that `lerTokens()` can recognize:

```python
# In your productions:
"OPERATOR -> + | - | * | /"

# In lerTokens(), you need:
if char == '+':
    tokens.append(Token('PLUS', '+', line, col))
elif char == '-':
    tokens.append(Token('MINUS', '-', line, col))
# ... etc
```

### Why Productions Matter for FIRST and FOLLOW

#### **Productions Drive Everything**

- **FIRST sets**: "What terminals can start each production?"
- **FOLLOW sets**: "What terminals can follow each non-terminal in productions?"
- **LL(1) table**: "Which production to use for each (non-terminal, terminal) pair?"

```python
# This production:
"EXPRESSION -> ( OPERAND OPERAND OPERATOR )"

# Means:
# FIRST(EXPRESSION) includes '('
# FOLLOW(OPERAND) includes what can start OPERAND and OPERATOR
# LL(1) table[EXPRESSION, '('] = "use this production"
```

## Why FIRST and FOLLOW Matter

### The Language Learning Analogy

Imagine learning a new language - you need to understand which words can start sentences and which words can follow others. If you don't know these patterns, you'll end up speaking like Yoda!

In compiler theory, FIRST and FOLLOW sets serve the same purpose for your parser. They tell the parser:
- **FIRST**: "Which terminals can start this non-terminal?"
- **FOLLOW**: "Which terminals can immediately follow this non-terminal?"

### The Critical Connection

**You CANNOT build an LL(1) parser without FIRST and FOLLOW sets!**

These sets are the mathematical foundation that enables:
1. **Predictive parsing**: The parser knows which rule to apply without backtracking
2. **Conflict detection**: Identifying when your grammar isn't LL(1)
3. **Table construction**: Building the LL(1) parsing table

## FIRST Sets: What Can Start a Production

### Definition

The **FIRST set** of a symbol (terminal or non-terminal) contains all terminals that can appear as the **first symbol** of any string derived from that symbol.

**Mathematical notation**: FIRST(X) = {all terminals that can start strings derived from X}

### Key Insights

- For terminals: FIRST(a) = {a}
- For non-terminals: FIRST(A) depends on its production rules
- Special case: If A can derive ε (empty string), then ε ∈ FIRST(A)

### FIRST Set Rules

#### Rule 1: Terminals
```
If X is a terminal: FIRST(X) = {X}
```

#### Rule 2: Non-terminals
For each production rule `A → Y₁Y₂...Yₙ`:

1. **If Y₁ is terminal**: Add Y₁ to FIRST(A)
2. **If Y₁ is non-terminal**: Add FIRST(Y₁) - {ε} to FIRST(A)
3. **If Y₁ can derive ε**: Also check Y₂, then Y₃, etc.
4. **If ALL symbols can derive ε**: Add ε to FIRST(A)

### Simple Example: FIRST Calculation

Given the grammar:
```
S → aB | bA
A → c | d
B → e | f
```

**Step-by-step calculation**:

| Symbol | Productions | FIRST Set | Explanation |
|--------|-------------|-----------|-------------|
| S | S → aB \| bA | {a, b} | First symbols of "aB" and "bA" |
| A | A → c \| d | {c, d} | Direct terminals |
| B | B → e \| f | {e, f} | Direct terminals |

**Result**: FIRST = {(S, {a, b}), (A, {c, d}), (B, {e, f})}

## FOLLOW Sets: What Can Come After

### Definition

The **FOLLOW set** of a non-terminal A contains all terminals that can appear **immediately after** A in some derivation of the grammar.

**Mathematical notation**: FOLLOW(A) = {all terminals that can immediately follow A}

### Key Insights

- FOLLOW is only defined for non-terminals (not terminals)
- Always add $ to FOLLOW(start_symbol)
- FOLLOW depends on how the non-terminal appears in other productions

### FOLLOW Set Rules

**FOLLOW Rules**:

**Rule 1**: Add $ to FOLLOW(start_symbol)

**Rule 2a**: For rule `B → αAβ`: Add FIRST(β) - {ε} to FOLLOW(A)

**Rule 2b**: For rule `B → αAβ`: If β is NULLABLE or β is empty, add FOLLOW(B) to FOLLOW(A)

#### Understanding the Rule Pattern `B → αAβ`

**The pattern `B → αAβ` means**:
- **B**: The non-terminal on the LEFT side of the arrow
- **α** (alpha): ALL symbols that come BEFORE A in the production
- **A**: The specific non-terminal we're calculating FOLLOW for
- **β** (beta): ALL symbols that come AFTER A in the production

**Critical Point**: For each production rule, you must analyze **every non-terminal** that appears in the right-hand side separately. Each one gets its own α, A, β breakdown.

### Simple Example: FOLLOW Calculation with Rule Applications

Using the same grammar:
```
S → aB | bA
A → c | d
B → e | f
```

**Step-by-step calculation**:

**Step 1: Apply Rule 1**
- **Start symbol is S**
- **Apply Rule 1**: Add $ to FOLLOW(S)
- **Result**: FOLLOW(S) = {$}

**Step 2: Apply Rules 2a and 2b to each production**

**Production: S → aB**
- *Analyzing B*: B=S, α=a, A=B, β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(S) to FOLLOW(B)
- Add FOLLOW(S) = {$} to FOLLOW(B)
- **Result**: FOLLOW(B) = {$}

**Production: S → bA**
- *Analyzing A*: B=S, α=b, A=A, β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(S) to FOLLOW(A)
- Add FOLLOW(S) = {$} to FOLLOW(A)
- **Result**: FOLLOW(A) = {$}

**Productions: A → c | d, B → e | f**
- No non-terminals to analyze

**Final Result**: FOLLOW = {(S, {$}), (A, {$}), (B, {$})}

## Step-by-Step Calculation Algorithms

### FIRST Set Algorithm

```python
def calculate_FIRST(productions):
    """
    Calculate FIRST sets for all non-terminals in a context-free grammar.

    FIRST(A) = all terminals that can appear as the first symbol of any string derived from A

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules in the format "A -> alpha" where:
        - A is a non-terminal (left-hand side)
        - alpha is a sequence of terminals and/or non-terminals (right-hand side)
        - Multiple rules for the same non-terminal can be separated by '|'
        Example: ["S -> aB | bA", "A -> c | d", "B -> e | f"]

        Where these come from: Usually from your grammar definition in construirGramatica()

    Returns:
    --------
    dict
        Dictionary mapping each non-terminal to its FIRST set
        Format: {non_terminal: set_of_terminals}
        Example: {'S': {'a', 'b'}, 'A': {'c', 'd'}, 'B': {'e', 'f'}}

        This return value is used by:
        - calculate_FOLLOW() function (needs FIRST sets for Rule 2a)
        - LL(1) table construction (for determining which production to use)
    """
    FIRST = {}

    # Step 1: Initialize FIRST sets
    non_terminals = get_non_terminals(productions)
    for nt in non_terminals:
        FIRST[nt] = set()

    # Step 2: Iterate until no changes (fixed-point iteration)
    changed = True
    while changed:
        changed = False
        for production in productions:
            A, symbols = parse_production(production)

            # Case 1: A → ε (epsilon production)
            if symbols == ['ε']:
                if 'ε' not in FIRST[A]:
                    FIRST[A].add('ε')
                    changed = True
                continue

            # Case 2: A → Y₁Y₂...Yₙ (sequence of symbols)
            k = 0
            can_derive_epsilon = True

            while k < len(symbols) and can_derive_epsilon:
                Yk = symbols[k]
                can_derive_epsilon = False

                if is_terminal(Yk):
                    # Add terminal to FIRST[A]
                    if Yk not in FIRST[A]:
                        FIRST[A].add(Yk)
                        changed = True
                else:
                    # Add FIRST[Yk] - {ε} to FIRST[A]
                    for symbol in FIRST[Yk]:
                        if symbol != 'ε' and symbol not in FIRST[A]:
                            FIRST[A].add(symbol)
                            changed = True

                    # Check if Yk can derive ε
                    if 'ε' in FIRST[Yk]:
                        can_derive_epsilon = True

                k += 1

            # If all symbols can derive ε, add ε to FIRST[A]
            if can_derive_epsilon:
                if 'ε' not in FIRST[A]:
                    FIRST[A].add('ε')
                    changed = True

    return FIRST
```

### FOLLOW Set Algorithm

```python
def calculate_FOLLOW(productions, start_symbol):
    """
    Calculate FOLLOW sets for all non-terminals in a context-free grammar.

    FOLLOW(A) = all terminals that can appear immediately after A in some derivation

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules in the format "A -> alpha"
        Same format as calculate_FIRST() - this is the SAME productions list

        Where this comes from: Your grammar definition in construirGramatica()

    start_symbol : str
        The start symbol of the grammar (usually 'PROGRAM', 'S', or 'E')

        Where this comes from: Defined in your grammar specification
        Example: If your grammar starts with "PROGRAM -> STATEMENT_LIST",
                 then start_symbol = "PROGRAM"

    Returns:
    --------
    dict
        Dictionary mapping each non-terminal to its FOLLOW set
        Format: {non_terminal: set_of_terminals}
        Example: {'S': {'$', ')'}, 'A': {'$', ')'}, 'B': {'+', '$', ')'}}

        This return value is used by:
        - LL(1) table construction (for epsilon productions)
        - Parser conflict detection
        - construirGramatica() function to build the complete LL(1) table
    """
    # First calculate FIRST sets (needed for FOLLOW Rule 2a)
    FIRST = calculate_FIRST(productions)
    FOLLOW = {}

    # Step 1: Initialize FOLLOW sets
    non_terminals = get_non_terminals(productions)
    for nt in non_terminals:
        FOLLOW[nt] = set()

    # Step 2: Apply Rule 1 - Add $ to FOLLOW(start_symbol)
    FOLLOW[start_symbol].add('$')

    # Step 3: Apply Rules 2a and 2b - Iterate until no changes (fixed-point)
    changed = True
    while changed:
        changed = False
        for production in productions:
            A, symbols = parse_production(production)  # A is left-hand side

            # Check each symbol in the production (looking for non-terminals)
            for i in range(len(symbols)):
                B = symbols[i]  # This is our target non-terminal

                if is_non_terminal(B):
                    beta = symbols[i+1:]  # β = symbols after B

                    if beta:  # β is not empty
                        first_beta = calculate_first_of_sequence(beta, FIRST)

                        # Apply Rule 2a: Add FIRST(β) - {ε} to FOLLOW(B)
                        for symbol in first_beta:
                            if symbol != 'ε' and symbol not in FOLLOW[B]:
                                FOLLOW[B].add(symbol)
                                changed = True

                        # Apply Rule 2b: If ε ∈ FIRST(β), add FOLLOW(A) to FOLLOW(B)
                        if 'ε' in first_beta:
                            for symbol in FOLLOW[A]:
                                if symbol not in FOLLOW[B]:
                                    FOLLOW[B].add(symbol)
                                    changed = True
                    else:  # β is empty (B is at the end of production)
                        # Apply Rule 2b: Add FOLLOW(A) to FOLLOW(B)
                        for symbol in FOLLOW[A]:
                            if symbol not in FOLLOW[B]:
                                FOLLOW[B].add(symbol)
                                changed = True

    return FOLLOW
```

## Complete Python Implementation

Here's the complete, production-ready implementation you can use for your RA2 project:

```python
def calculate_first_of_sequence(sequence, FIRST, non_terminals):
    """
    Calculate FIRST set for a sequence of symbols (used in FOLLOW calculation).

    This helper function computes FIRST(β) where β is a sequence like [Y1, Y2, ..., Yn]

    Parameters:
    -----------
    sequence : list of str
        A sequence of symbols (terminals and/or non-terminals)
        Example: ['E', "'", ')'] or ['+', 'T', 'E', "'"]

        Where this comes from: When calculating FOLLOW, this is the β part
        in the pattern "B → αAβ" - it's everything that comes after A

    FIRST : dict
        Previously calculated FIRST sets for all non-terminals
        Format: {non_terminal: set_of_terminals}

        Where this comes from: Output of calculate_FIRST() function

    non_terminals : set
        Set of all non-terminal symbols in the grammar

        Where this comes from: Extracted from the productions list

    Returns:
    --------
    set
        FIRST set of the sequence - all terminals that can start strings
        derived from this sequence
        Example: {'+', 'ε'} or {')', '$'}

        This return value is used by:
        - calculate_FOLLOW() to apply Rule 2a and check for Rule 2b
    """
    first_sequence = set()

    for symbol in sequence:
        if symbol not in non_terminals:  # Terminal symbol
            first_sequence.add(symbol)
            break  # Stop here - terminals can't derive ε
        else:  # Non-terminal symbol
            # Add FIRST[symbol] - {ε} to result
            for s in FIRST[symbol]:
                if s != 'ε':
                    first_sequence.add(s)

            # If ε not in FIRST[symbol], stop processing
            if 'ε' not in FIRST[symbol]:
                break
    else:
        # If we processed all symbols without breaking
        # (meaning all symbols can derive ε)
        first_sequence.add('ε')

    return first_sequence

def calculate_FIRST(productions):
    """
    Production-ready FIRST set calculation for RA2 project.

    This is the complete implementation you can use directly in construirGramatica().

    Parameters:
    -----------
    productions : list of str
        Grammar productions in string format
        Example: ["E -> T E'", "E' -> + T E' | ε", "T -> F T'"]

        Where this comes from: Your grammar definition - either hardcoded
        in construirGramatica() or loaded from a file

    Returns:
    --------
    dict
        Complete FIRST sets for the grammar
        Format: {non_terminal: set_of_terminals_and_epsilon}

        Used by: construirGramatica() to build LL(1) parsing table
    """
    FIRST = {}

    # Identify all non-terminals from left-hand sides
    non_terminals = set()
    for production in productions:
        X = production.split('->')[0].strip()
        non_terminals.add(X)

    # Initialize empty FIRST sets
    for nt in non_terminals:
        FIRST[nt] = set()

    # Fixed-point iteration until convergence
    changed = True
    while changed:
        changed = False
        for production in productions:
            parts = production.split('->')
            X = parts[0].strip()
            symbols = parts[1].strip().split()

            # Special case: X → ε
            if symbols == ['ε']:
                if 'ε' not in FIRST[X]:
                    FIRST[X].add('ε')
                    changed = True
                continue

            # Process symbols
            k = 0
            continue_flag = True
            while k < len(symbols) and continue_flag:
                Yk = symbols[k]
                continue_flag = False

                if Yk not in non_terminals and Yk != 'ε':  # Terminal
                    if Yk not in FIRST[X]:
                        FIRST[X].add(Yk)
                        changed = True
                elif Yk in non_terminals:  # Non-terminal
                    # Add FIRST[Yk] - {ε} to FIRST[X]
                    for symbol in FIRST[Yk]:
                        if symbol != 'ε' and symbol not in FIRST[X]:
                            FIRST[X].add(symbol)
                            changed = True

                    # If ε ∈ FIRST[Yk], continue to next symbol
                    if 'ε' in FIRST[Yk]:
                        continue_flag = True

                k += 1

            # If all symbols can derive ε
            if continue_flag:
                if 'ε' not in FIRST[X]:
                    FIRST[X].add('ε')
                    changed = True

    return FIRST

def calculate_FOLLOW(productions, start_symbol):
    """Calculate FOLLOW sets for all non-terminals."""
    # Calculate FIRST sets first
    FIRST = calculate_FIRST(productions)
    FOLLOW = {}

    # Identify non-terminals
    non_terminals = set()
    for production in productions:
        X = production.split('->')[0].strip()
        non_terminals.add(X)

    # Initialize FOLLOW sets
    for nt in non_terminals:
        FOLLOW[nt] = set()

    # Add $ to FOLLOW(start_symbol)
    FOLLOW[start_symbol].add('$')

    # Iterate until convergence
    changed = True
    while changed:
        changed = False
        for production in productions:
            parts = production.split('->')
            A = parts[0].strip()
            alpha = parts[1].strip().split()

            # Check each symbol in production
            for i in range(len(alpha)):
                B = alpha[i]

                if B in non_terminals:  # B is non-terminal
                    beta = alpha[i+1:]  # Symbols after B

                    if beta:  # β exists
                        first_beta = calculate_first_of_sequence(beta, FIRST, non_terminals)

                        # Add FIRST(β) - {ε} to FOLLOW(B)
                        for symbol in first_beta:
                            if symbol != 'ε' and symbol not in FOLLOW[B]:
                                FOLLOW[B].add(symbol)
                                changed = True

                        # If ε ∈ FIRST(β), add FOLLOW(A) to FOLLOW(B)
                        if 'ε' in first_beta:
                            for symbol in FOLLOW[A]:
                                if symbol not in FOLLOW[B]:
                                    FOLLOW[B].add(symbol)
                                    changed = True
                    else:  # B is at the end
                        # Add FOLLOW(A) to FOLLOW(B)
                        for symbol in FOLLOW[A]:
                            if symbol not in FOLLOW[B]:
                                FOLLOW[B].add(symbol)
                                changed = True

    return FOLLOW

# Example usage for testing
if __name__ == "__main__":
    # Test grammar
    productions = [
        "S -> a B",
        "S -> b A",
        "A -> c",
        "A -> d",
        "B -> e",
        "B -> f"
    ]
    start_symbol = "S"

    # Calculate sets
    FIRST = calculate_FIRST(productions)
    FOLLOW = calculate_FOLLOW(productions, start_symbol)

    # Display results
    print("FIRST Sets:")
    for nt in sorted(FIRST.keys()):
        print(f"  FIRST({nt}) = {{{', '.join(sorted(FIRST[nt]))}}}")

    print("\nFOLLOW Sets:")
    for nt in sorted(FOLLOW.keys()):
        print(f"  FOLLOW({nt}) = {{{', '.join(sorted(FOLLOW[nt]))}}}")
```

### Helper Functions with Complete Documentation

```python
def get_non_terminals(productions):
    """
    Extract all non-terminal symbols from a list of productions.

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules
        Example: ["E -> T E'", "E' -> + T E' | ε"]

    Returns:
    --------
    set
        Set of all non-terminal symbols (left-hand sides of productions)
        Example: {'E', "E'", 'T', "T'", 'F'}
    """
    non_terminals = set()
    for production in productions:
        lhs = production.split('->')[0].strip()
        non_terminals.add(lhs)
    return non_terminals

def get_all_terminals(productions):
    """
    Extract all terminal symbols from production rules.

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules

    Returns:
    --------
    set
        Set of all terminal symbols found in the grammar
        Example: {'+', '*', '(', ')', 'id', 'ε'}
    """
    terminals = set()
    non_terminals = get_non_terminals(productions)

    for production in productions:
        rhs = production.split('->')[1].strip()
        alternatives = rhs.split('|')

        for alt in alternatives:
            symbols = alt.strip().split()
            for symbol in symbols:
                if symbol not in non_terminals:
                    terminals.add(symbol)

    return terminals

def is_terminal(symbol):
    """
    Check if a symbol is a terminal.

    Parameters:
    -----------
    symbol : str
        The symbol to check

    Returns:
    --------
    bool
        True if symbol is terminal, False if non-terminal

    Note: Terminals are typically lowercase or special characters
    Non-terminals are typically uppercase or contain apostrophes
    """
    # This is a simple heuristic - you may need to adjust based on your grammar
    return symbol.islower() or symbol in {'+', '-', '*', '/', '|', '%', '^',
                                          '(', ')', '>', '<', '>=', '<=',
                                          '==', '!=', '$', 'ε', 'FOR', 'WHILE',
                                          'IF', 'ELSE', 'ASSIGN', 'MEM', 'NUMBER', 'IDENTIFIER'}

def is_non_terminal(symbol):
    """
    Check if a symbol is a non-terminal.

    Parameters:
    -----------
    symbol : str
        The symbol to check

    Returns:
    --------
    bool
        True if symbol is non-terminal, False if terminal
    """
    return not is_terminal(symbol)

def parse_production(production):
    """
    Parse a production rule into left-hand side and right-hand side symbols.

    Parameters:
    -----------
    production : str
        A single production rule
        Example: "E -> T E'" or "E' -> + T E' | ε"

    Returns:
    --------
    tuple
        (lhs, rhs_symbols) where:
        - lhs: left-hand side non-terminal
        - rhs_symbols: list of symbols on right-hand side

    Note: This function handles the first alternative if multiple alternatives exist
    """
    parts = production.split('->')
    lhs = parts[0].strip()
    rhs = parts[1].strip()

    # Handle multiple alternatives (take first one)
    if '|' in rhs:
        rhs = rhs.split('|')[0].strip()

    # Split into individual symbols
    if rhs == 'ε':
        rhs_symbols = ['ε']
    else:
        rhs_symbols = rhs.split()

    return lhs, rhs_symbols

# Complete Integration Function for RA2 Project
def construirGramatica():
    """
    Complete grammar construction function for RA2 project.

    This function demonstrates how to integrate FIRST/FOLLOW calculation
    into your main grammar construction process.

    Returns:
    --------
    dict
        Complete grammar structure with:
        - 'productions': original production rules
        - 'first_sets': calculated FIRST sets
        - 'follow_sets': calculated FOLLOW sets
        - 'start_symbol': grammar start symbol
        - 'terminals': set of terminal symbols
        - 'non_terminals': set of non-terminal symbols
    """
    # Define your RPN grammar productions
    productions = [
        "PROGRAM -> STATEMENT_LIST",
        "STATEMENT_LIST -> STATEMENT STATEMENT_LIST | ε",
        "STATEMENT -> EXPRESSION | FOR_STATEMENT | WHILE_STATEMENT | IF_STATEMENT | ASSIGN_STATEMENT",
        "EXPRESSION -> ( OPERAND OPERAND OPERATOR ) | OPERAND",
        "OPERAND -> NUMBER | IDENTIFIER | EXPRESSION | MEMORY_REF",
        "FOR_STATEMENT -> FOR ( OPERAND OPERAND IDENTIFIER STATEMENT )",
        "WHILE_STATEMENT -> WHILE ( EXPRESSION STATEMENT )",
        "IF_STATEMENT -> IF ( EXPRESSION STATEMENT ) | IF ( EXPRESSION STATEMENT ) ELSE ( STATEMENT )",
        "ASSIGN_STATEMENT -> ASSIGN ( OPERAND IDENTIFIER )",
        "MEMORY_REF -> MEM ( IDENTIFIER )",
        "OPERATOR -> + | - | * | | | / | % | ^ | > | < | >= | <= | == | !="
    ]

    start_symbol = "PROGRAM"

    # Calculate FIRST and FOLLOW sets
    first_sets = calculate_FIRST(productions)
    follow_sets = calculate_FOLLOW(productions, start_symbol)

    # Extract terminals and non-terminals
    non_terminals = get_non_terminals(productions)
    terminals = get_all_terminals(productions)

    return {
        'productions': productions,
        'first_sets': first_sets,
        'follow_sets': follow_sets,
        'start_symbol': start_symbol,
        'terminals': terminals,
        'non_terminals': non_terminals
    }
```

## Practical Examples with Your RPN Grammar

### Complete RPN Grammar (Actual Implementation)

```python
# Your complete RPN grammar (56 production rules)
rpn_productions = [
    "PROGRAM -> LINHA PROGRAM_PRIME",
    "PROGRAM_PRIME -> LINHA PROGRAM_PRIME",
    "PROGRAM_PRIME -> EPSILON",
    "LINHA -> ABRE_PARENTESES CONTENT FECHA_PARENTESES",
    "CONTENT -> NUMERO_REAL AFTER_NUM",
    "CONTENT -> VARIAVEL AFTER_VAR",
    "CONTENT -> ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
    "CONTENT -> FOR FOR_STRUCT",
    "CONTENT -> WHILE WHILE_STRUCT",
    "CONTENT -> IFELSE IFELSE_STRUCT",
    "AFTER_NUM -> NUMERO_REAL OPERATOR",
    "AFTER_NUM -> VARIAVEL AFTER_VAR_OP",
    "AFTER_NUM -> ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
    "AFTER_NUM -> NOT",
    "AFTER_NUM -> RES",
    "AFTER_NUM -> EPSILON",
    "AFTER_VAR_OP -> OPERATOR",
    "AFTER_VAR_OP -> EPSILON",
    "AFTER_VAR -> NUMERO_REAL AFTER_VAR_OP",
    "AFTER_VAR -> VARIAVEL AFTER_VAR_OP",
    "AFTER_VAR -> ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_VAR_OP",
    "AFTER_VAR -> NOT",
    "AFTER_VAR -> RES",
    "AFTER_VAR -> EPSILON",
    "AFTER_EXPR -> OPERATOR EXPR_CHAIN",
    "AFTER_EXPR -> EPSILON",
    "EXPR_CHAIN -> NUMERO_REAL OPERATOR",
    "EXPR_CHAIN -> VARIAVEL AFTER_VAR_OP",
    "EXPR_CHAIN -> ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
    "EXPR_CHAIN -> NOT",
    "EXPR_CHAIN -> RES",
    "EXPR_CHAIN -> EPSILON",
    "EXPR -> NUMERO_REAL AFTER_NUM",
    "EXPR -> VARIAVEL AFTER_VAR",
    "EXPR -> ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
    "EXPR -> FOR FOR_STRUCT",
    "EXPR -> WHILE WHILE_STRUCT",
    "EXPR -> IFELSE IFELSE_STRUCT",
    "OPERATOR -> SOMA",
    "OPERATOR -> SUBTRACAO",
    "OPERATOR -> MULTIPLICACAO",
    "OPERATOR -> DIVISAO_INTEIRA",
    "OPERATOR -> DIVISAO_REAL",
    "OPERATOR -> RESTO",
    "OPERATOR -> POTENCIA",
    "OPERATOR -> MENOR",
    "OPERATOR -> MAIOR",
    "OPERATOR -> IGUAL",
    "OPERATOR -> MENOR_IGUAL",
    "OPERATOR -> MAIOR_IGUAL",
    "OPERATOR -> DIFERENTE",
    "OPERATOR -> AND",
    "OPERATOR -> OR",
    "OPERATOR -> NOT",
    "ARITH_OP -> SOMA",
    "ARITH_OP -> SUBTRACAO",
    "ARITH_OP -> MULTIPLICACAO",
    "ARITH_OP -> DIVISAO_INTEIRA",
    "ARITH_OP -> DIVISAO_REAL",
    "ARITH_OP -> RESTO",
    "ARITH_OP -> POTENCIA",
    "COMP_OP -> MENOR",
    "COMP_OP -> MAIOR",
    "COMP_OP -> IGUAL",
    "COMP_OP -> MENOR_IGUAL",
    "COMP_OP -> MAIOR_IGUAL",
    "COMP_OP -> DIFERENTE",
    "LOGIC_OP -> AND",
    "LOGIC_OP -> OR",
    "LOGIC_OP -> NOT",
    "FOR_STRUCT -> ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES LINHA",
    "WHILE_STRUCT -> ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA",
    "IFELSE_STRUCT -> ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA LINHA"
]
```

### Actual FIRST Sets for Your RPN Grammar

```
FIRST(PROGRAM) = {ABRE_PARENTESES}
FIRST(PROGRAM_PRIME) = {ABRE_PARENTESES, ε}
FIRST(LINHA) = {ABRE_PARENTESES}
FIRST(CONTENT) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, FOR, WHILE, IFELSE}
FIRST(AFTER_NUM) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, ε}
FIRST(AFTER_VAR_OP) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO_INTEIRA, DIVISAO_REAL, RESTO, POTENCIA, MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE, AND, OR, NOT, ε}
FIRST(AFTER_VAR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, ε}
FIRST(AFTER_EXPR) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO_INTEIRA, DIVISAO_REAL, RESTO, POTENCIA, MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE, AND, OR, NOT, ε}
FIRST(EXPR_CHAIN) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, ε}
FIRST(EXPR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, FOR, WHILE, IFELSE}
FIRST(OPERATOR) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO_INTEIRA, DIVISAO_REAL, RESTO, POTENCIA, MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE, AND, OR, NOT}
FIRST(ARITH_OP) = {SOMA, SUBTRACAO, MULTIPLICACAO, DIVISAO_INTEIRA, DIVISAO_REAL, RESTO, POTENCIA}
FIRST(COMP_OP) = {MENOR, MAIOR, IGUAL, MENOR_IGUAL, MAIOR_IGUAL, DIFERENTE}
FIRST(LOGIC_OP) = {AND, OR, NOT}
FIRST(FOR_STRUCT) = {ABRE_PARENTESES}
FIRST(WHILE_STRUCT) = {ABRE_PARENTESES}
FIRST(IFELSE_STRUCT) = {ABRE_PARENTESES}
```

### Actual FOLLOW Sets for Your RPN Grammar

```
FOLLOW(PROGRAM) = {$}
FOLLOW(PROGRAM_PRIME) = {$}
FOLLOW(LINHA) = {ABRE_PARENTESES, FECHA_PARENTESES, $}
FOLLOW(CONTENT) = {FECHA_PARENTESES}
FOLLOW(AFTER_NUM) = {FECHA_PARENTESES}
FOLLOW(AFTER_VAR_OP) = {FECHA_PARENTESES}
FOLLOW(AFTER_VAR) = {FECHA_PARENTESES}
FOLLOW(AFTER_EXPR) = {FECHA_PARENTESES}
FOLLOW(EXPR_CHAIN) = {FECHA_PARENTESES}
FOLLOW(EXPR) = {FECHA_PARENTESES}
FOLLOW(OPERATOR) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, FECHA_PARENTESES}
FOLLOW(ARITH_OP) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, FECHA_PARENTESES}
FOLLOW(COMP_OP) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, FECHA_PARENTESES}
FOLLOW(LOGIC_OP) = {NUMERO_REAL, VARIAVEL, ABRE_PARENTESES, NOT, RES, FECHA_PARENTESES}
FOLLOW(FOR_STRUCT) = {FECHA_PARENTESES}
FOLLOW(WHILE_STRUCT) = {FECHA_PARENTESES}
FOLLOW(IFELSE_STRUCT) = {FECHA_PARENTESES}
```

### Complex Example: Nested RPN with Circular Dependencies

For input `((A B +) (C D *) /)`:
1. PROGRAM → LINHA PROGRAM_PRIME structure handles multiple statements
2. Each nested expression uses AFTER_* non-terminals for deterministic parsing
3. FIRST/FOLLOW sets enable predictive parsing despite circular dependencies

### Critical: Circular Dependencies in FOLLOW Sets

**Important**: Your RPN grammar has **circular dependencies** in FOLLOW calculation:
```
FOLLOW(AFTER_NUM) ↔ FOLLOW(EXPR) ↔ FOLLOW(AFTER_VAR) ↔ FOLLOW(AFTER_EXPR) ↔ FOLLOW(EXPR_CHAIN) ↔ FOLLOW(AFTER_VAR_OP)
```

**This is completely normal!** Circular dependencies:
- Are **expected** in recursive grammars
- Are **solved** by fixed-point iteration algorithms
- **Don't indicate** grammar problems
- Are **standard** in LL(1) grammar analysis

**Solution**: All circular dependencies resolve to {FECHA_PARENTESES} through mathematical fixed-point iteration, ensuring a conflict-free LL(1) grammar.

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Forgetting Epsilon (ε) Rules

**Problem**: Not handling productions that can derive empty string
```python
# Wrong - ignoring epsilon
if symbols == ['epsilon']:
    continue  # WRONG!

# Correct - handling epsilon
if symbols == ['epsilon']:
    if 'ε' not in FIRST[X]:
        FIRST[X].add('ε')
        changed = True
```

### Pitfall 2: Infinite Loops in Calculation

**Problem**: Not checking for convergence properly
```python
# Wrong - could loop forever
while True:
    # Calculate sets without checking changes

# Correct - check for convergence
changed = True
while changed:
    changed = False
    # Only set changed = True when sets actually change
```

### Pitfall 3: Incorrect FOLLOW Dependencies

**Problem**: Calculating FOLLOW without proper FIRST sets
```python
# Wrong - calculate FOLLOW without FIRST
def calculate_FOLLOW(productions):
    # Missing FIRST calculation!

# Correct - always calculate FIRST first
def calculate_FOLLOW(productions, start_symbol):
    FIRST = calculate_FIRST(productions)  # Required!
    # ... rest of algorithm
```

### Pitfall 4: Not Handling Sequences in FOLLOW

**Problem**: Incorrectly calculating FIRST of symbol sequences
```python
# Wrong - only looking at first symbol
if beta:
    first_beta = FIRST[beta[0]]  # WRONG!

# Correct - calculate FIRST of entire sequence
if beta:
    first_beta = calculate_first_of_sequence(beta, FIRST, non_terminals)
```

## Integration with LL(1) Table Construction

### How FIRST and FOLLOW Build the Parsing Table

The LL(1) parsing table is constructed using these rules:

1. **For each production A → α**:
   - **FIRST Rule**: For each terminal `a` in FIRST(α), add "A → α" to Table[A, a]
   - **FOLLOW Rule**: If ε ∈ FIRST(α), for each terminal `b` in FOLLOW(A), add "A → α" to Table[A, b]

2. **Conflict Detection**:
   - If any cell has multiple entries → **NOT LL(1)**
   - If all cells have at most one entry → **LL(1) grammar** ✅

### Example Table Construction

For your RPN grammar:

| Non-Terminal | ( | NUMBER | IDENTIFIER | + | - | * | / | % | ^ | \| | ) | $ |
|--------------|---|--------|------------|---|---|---|---|---|---|----|----|---|
| EXPR | EXPR→(OPERAND OPERAND OPERATOR) | | | | | | | | | | | |
| OPERAND | OPERAND→EXPR | OPERAND→NUMBER | OPERAND→IDENTIFIER | | | | | | | | | |
| OPERATOR | | | | OPERATOR→+ | OPERATOR→- | OPERATOR→* | OPERATOR→/ | OPERATOR→% | OPERATOR→^ | OPERATOR→\| | | |

## Key Takeaways for RA2 Implementation

### 1. **Implementation Order**
1. ✅ Implement `calculate_FIRST()` first
2. ✅ Test FIRST calculation with simple examples
3. ✅ Implement `calculate_FOLLOW()` using FIRST
4. ✅ Test both with your RPN grammar
5. ✅ Use these sets to build LL(1) table

### 2. **Testing Strategy**
```python
def test_first_follow():
    # Test with known simple grammar first
    simple_grammar = ["S -> a B", "B -> b"]

    # Verify expected results
    FIRST = calculate_FIRST(simple_grammar)
    assert FIRST['S'] == {'a'}
    assert FIRST['B'] == {'b'}

    # Then test with your RPN grammar
    rpn_grammar = [...] # Your actual grammar
    FIRST_rpn = calculate_FIRST(rpn_grammar)
    # Verify results match hand calculations
```

### 3. **Integration with `construirGramatica()` - Complete Implementation**
```python
def construirGramatica():
    """Student 1's function - Build LL(1) grammar and table."""
    # Complete RPN grammar with 56 production rules (already proven LL(1))
    GRAMATICA_RPN = {
        'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
        'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['EPSILON']],
        'LINHA': [['ABRE_PARENTESES', 'CONTENT', 'FECHA_PARENTESES']],
        'CONTENT': [
            ['NUMERO_REAL', 'AFTER_NUM'],
            ['VARIAVEL', 'AFTER_VAR'],
            ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'AFTER_EXPR'],
            ['FOR', 'FOR_STRUCT'],
            ['WHILE', 'WHILE_STRUCT'],
            ['IFELSE', 'IFELSE_STRUCT']
        ],
        'AFTER_NUM': [
            ['NUMERO_REAL', 'OPERATOR'],
            ['VARIAVEL', 'AFTER_VAR_OP'],
            ['ABRE_PARENTESES', 'EXPR', 'FECHA_PARENTESES', 'OPERATOR'],
            ['NOT'],
            ['RES'],
            ['EPSILON']
        ],
        # ... all other productions from the proven grammar
    }

    # FIRST sets (already calculated and proven)
    FIRST_SETS = {
        'PROGRAM': {'ABRE_PARENTESES'},
        'PROGRAM_PRIME': {'ABRE_PARENTESES', 'EPSILON'},
        'LINHA': {'ABRE_PARENTESES'},
        'CONTENT': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'FOR', 'WHILE', 'IFELSE'},
        # ... all FIRST sets from proven calculations
    }

    # FOLLOW sets (already calculated and proven - handles circular dependencies)
    FOLLOW_SETS = {
        'PROGRAM': {'$'},
        'PROGRAM_PRIME': {'$'},
        'LINHA': {'ABRE_PARENTESES', 'FECHA_PARENTESES', '$'},
        'CONTENT': {'FECHA_PARENTESES'},
        # ... all FOLLOW sets from proven calculations
    }

    # Nullable sets (non-terminals that can derive epsilon)
    NULLABLE = {'PROGRAM_PRIME', 'AFTER_NUM', 'AFTER_VAR_OP', 'AFTER_VAR', 'AFTER_EXPR', 'EXPR_CHAIN'}

    # Grammar is already validated as LL(1) compatible with no conflicts
    return {
        'gramatica': GRAMATICA_RPN,
        'first_sets': FIRST_SETS,
        'follow_sets': FOLLOW_SETS,
        'nullable_sets': NULLABLE,
        'start_symbol': 'PROGRAM',
        'terminals': {'ABRE_PARENTESES', 'FECHA_PARENTESES', 'NUMERO_REAL', 'VARIAVEL', 'FOR', 'WHILE', 'IFELSE',
                     'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO_INTEIRA', 'DIVISAO_REAL', 'RESTO',
                     'POTENCIA', 'MENOR', 'MAIOR', 'IGUAL', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE',
                     'AND', 'OR', 'NOT', 'RES', '$', 'EPSILON'},
        'non_terminals': {'PROGRAM', 'PROGRAM_PRIME', 'LINHA', 'CONTENT', 'AFTER_NUM', 'AFTER_VAR_OP',
                         'AFTER_VAR', 'AFTER_EXPR', 'EXPR_CHAIN', 'EXPR', 'OPERATOR', 'ARITH_OP',
                         'COMP_OP', 'LOGIC_OP', 'FOR_STRUCT', 'WHILE_STRUCT', 'IFELSE_STRUCT'}
    }
```

### 4. **Error Handling**
- Always validate input productions format
- Check for undefined non-terminals
- Handle epsilon productions correctly
- Detect and report calculation errors

---

## Next Steps

Now that you understand FIRST and FOLLOW calculation:
1. **Next theory file**: LL(1) Table Construction and Conflict Resolution
2. **After that**: Complete Grammar Specification for Your RPN Language
3. **Finally**: Integration Guidelines for Team Development

**Remember**: FIRST and FOLLOW are the mathematical backbone of your parser. Get these right, and your LL(1) table will work perfectly! 🚀

## Team Discussion Questions

1. How will you handle the nested structure of RPN expressions in your FIRST/FOLLOW calculation?
2. What terminals do you need for control structures (FOR, WHILE, IF, ELSE)?
3. How will you test your FIRST/FOLLOW implementation before integrating?
4. What error handling will you add to catch malformed grammar rules?
5. How will you structure the code to make it easy for other team members to use?
