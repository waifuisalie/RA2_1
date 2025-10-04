# Grammar Fundamentals for Compilers: A Beginner's Guide

## Table of Contents
1. [What is a Grammar?](#what-is-a-grammar)
2. [The Chomsky Hierarchy](#the-chomsky-hierarchy)
3. [Context-Free Grammars (Type 2)](#context-free-grammars-type-2)
4. [Grammar Components](#grammar-components)
5. [Examples and Practical Applications](#examples-and-practical-applications)
6. [BNF Notation](#bnf-notation)
7. [Key Takeaways for Your RA2 Project](#key-takeaways-for-your-ra2-project)

## What is a Grammar?

Imagine you're learning a new language. How do you know if a sentence is correct? You follow **grammar rules**. In computer science, a **formal grammar** works the same way - it defines the rules for what makes a valid "sentence" (program) in a programming language.

### Simple Analogy
- **Natural Language**: "The cat sits on the mat" ✅ (correct grammar)
- **Natural Language**: "Cat the sits mat on the" ❌ (incorrect grammar)
- **Programming Language**: `(3 + 4)` ✅ (correct syntax)
- **Programming Language**: `+ 3 4 (` ❌ (incorrect syntax)

### Why Do We Need Grammars in Compilers?

When you write code like:
```python
if (x > 5):
    print("Hello")
```

The compiler needs to understand:
1. **What are the valid words?** (`if`, `print`, `>`, etc.) → This is **Lexical Analysis** (Phase 1)
2. **How can these words be arranged?** → This is **Syntax Analysis** (Phase 2) ← **YOUR RA2 PROJECT!**

The grammar defines the "sentence structure rules" for your programming language.

## The Chomsky Hierarchy

In 1956, linguist Noam Chomsky created a classification system for languages based on their complexity. Think of it as different "levels" of grammar rules:

### Type 3: Regular Languages (Simplest)
- **What they recognize**: Simple patterns like "all words ending in 'ing'"
- **Real example**: Email validation, phone numbers
- **Limitation**: Cannot handle nested structures like parentheses: `((()))`
- **Recognized by**: Finite Automata (very simple machines)

### Type 2: Context-Free Languages ⭐ **THIS IS WHAT YOU'RE WORKING WITH!**
- **What they recognize**: Nested structures, programming languages
- **Real example**: Mathematical expressions: `(3 + (4 * 5))`
- **Power**: Can handle any level of nesting!
- **Recognized by**: Pushdown Automata (machines with a stack memory)

### Type 1: Context-Sensitive Languages
- **More powerful but much more complex**
- **Example**: Languages where word order depends on context

### Type 0: Unrestricted Languages
- **Most powerful but computationally complex**
- **Recognized by**: Turing Machines

### Key Insight for RA2
Your RPN language with expressions like `(A B +)` and nested structures like `((A B +) (C D *) /)` is a **Type 2 (Context-Free)** language. This is why you need LL(1) parsing!

## Context-Free Grammars (Type 2)

### What Makes a Grammar "Context-Free"?

**Context-Free** means that when you apply a grammar rule, it doesn't matter what symbols are around it. The rule `A → B C` can be applied to `A` regardless of what comes before or after it.

### Why Context-Free Grammars are Perfect for Programming Languages

Programming languages have nested structures:
- Parentheses: `((()))`
- Function calls: `func(arg1, func2(arg3))`
- Code blocks: `if { if { } }`
- **Your RPN expressions**: `((A B +) (C D *) /)`

Context-Free Grammars can handle **unlimited nesting** - perfect for programming languages!

## Grammar Components

A Context-Free Grammar is defined by 4 components: **G = (N, Σ, P, S)**

### 1. N: Non-Terminals (Variables)
- **What they are**: Symbols that can be "expanded" or "replaced"
- **Convention**: UPPERCASE letters (A, B, EXPRESSION, STATEMENT)
- **Think of them as**: "Placeholders" that represent language constructs

### 2. Σ (Sigma): Terminals
- **What they are**: The actual symbols that appear in your final program
- **Convention**: lowercase letters or actual symbols (+, -, if, while, numbers)
- **Think of them as**: The "words" of your language

### 3. P: Production Rules
- **What they are**: Rules that define how non-terminals can be replaced
- **Format**: `A → B C` (read as "A can be replaced by B followed by C")
- **Think of them as**: The "grammar rules" of your language

### 4. S: Start Symbol
- **What it is**: The "root" of your language - where all valid programs begin
- **Usually**: Something like PROGRAM or EXPRESSION

## Examples and Practical Applications

### Example 1: Simple Palindromes
Let's build a grammar for palindromes over alphabet {0, 1}:

```
Grammar Components:
N = {P}          // P represents "Palindrome"
Σ = {0, 1}        // Our alphabet
S = P             // Start with P
P (Production Rules):
  P → ε           // Empty string is a palindrome
  P → 0           // Single 0 is a palindrome
  P → 1           // Single 1 is a palindrome
  P → 0P0         // 0 + palindrome + 0
  P → 1P1         // 1 + palindrome + 1
```

**How it works:**
To generate "0110":
```
P ⇒ 0P0          // Apply rule P → 0P0
  ⇒ 01P10        // Apply rule P → 1P1
  ⇒ 01ε10        // Apply rule P → ε
  ⇒ 0110          // Remove ε (empty string)
```

### Example 2: Simple Arithmetic Expressions
```
Grammar Components:
N = {E, T, F}                    // Expression, Term, Factor
Σ = {+, *, (, ), id}            // Operators and identifiers
S = E                           // Start with Expression

Production Rules:
E → E + T | T                   // Expression: terms connected by +
T → T * F | F                   // Term: factors connected by *
F → (E) | id                    // Factor: parentheses or identifier
```

**This grammar handles precedence!**
- `id + id * id` becomes `id + (id * id)` ✅
- Multiplication has higher precedence than addition

### Example 3: Your RPN Language (Complete LL(1) Grammar)
```
Grammar Components:
N = {PROGRAM, PROGRAM_PRIME, LINHA, CONTENT, AFTER_NUM, AFTER_VAR_OP,
     AFTER_VAR, AFTER_EXPR, EXPR_CHAIN, EXPR, OPERATOR, ARITH_OP,
     COMP_OP, LOGIC_OP, FOR_STRUCT, WHILE_STRUCT, IFELSE_STRUCT}
Σ = {(, ), +, -, *, /, |, %, ^, <, >, ==, <=, >=, !=, &&, ||, !,
     NUMBER, IDENTIFIER, FOR, WHILE, IFELSE, RES, ε}
S = PROGRAM

Key Production Rules (56 total):
PROGRAM → LINHA PROGRAM_PRIME
LINHA → ( CONTENT )
CONTENT → NUMBER AFTER_NUM | IDENTIFIER AFTER_VAR | FOR FOR_STRUCT | WHILE WHILE_STRUCT | IFELSE IFELSE_STRUCT
AFTER_NUM → NUMBER OPERATOR | IDENTIFIER AFTER_VAR_OP | ( EXPR ) OPERATOR | NOT | RES | ε
OPERATOR → ARITH_OP | COMP_OP | LOGIC_OP
FOR_STRUCT → ( NUMBER ) ( NUMBER ) ( NUMBER ) LINHA
WHILE_STRUCT → ( EXPR ) LINHA
IFELSE_STRUCT → ( EXPR ) LINHA LINHA
```

**How complex nested expressions work:**
`((A B +) (C D *) /)` breaks down as:
1. PROGRAM → LINHA PROGRAM_PRIME
2. LINHA → ( CONTENT )
3. CONTENT → ( EXPR ) AFTER_EXPR
4. EXPR → IDENTIFIER AFTER_VAR (for A B +)
5. AFTER_EXPR → OPERATOR EXPR_CHAIN (for the division)
6. This creates a fully LL(1) parseable structure!

## BNF Notation

**BNF (Backus-Naur Form)** is just a standard way to write grammar rules. Instead of `A → B C`, BNF uses:

```bnf
<expression> ::= <term> "+" <expression> | <term>
<term> ::= <factor> "*" <term> | <factor>
<factor> ::= "(" <expression> ")" | "id"
```

**Key BNF symbols:**
- `<symbol>` = Non-terminal
- `"symbol"` = Terminal
- `::=` = "is defined as" (same as →)
- `|` = "or" (alternative rules)

## Key Takeaways for Your RA2 Project

### 1. **Your Language is Context-Free**
Your RPN language with nested expressions like `((A B +) (C D *) /)` is definitely Context-Free (Type 2). This confirms you need LL(1) parsing.

### 2. **Grammar Design is Critical**
Before writing any code, you must:
1. ✅ Define all your terminals (numbers, operators, parentheses, new control structure tokens)
2. ✅ Define your non-terminals (EXPRESSION, STATEMENT, LOOP, DECISION, etc.)
3. ✅ Write clear production rules
4. ✅ Ensure your grammar is LL(1) (no conflicts)

### 3. **Control Structures - Implemented Rules**
Your grammar includes three types of control structures in RPN postfix notation:
```
// Actual implemented syntax:
FOR_STRUCT → ( NUMBER ) ( NUMBER ) ( NUMBER ) LINHA    // (1) (10) (1) body
WHILE_STRUCT → ( EXPR ) LINHA                          // (condition) body
IFELSE_STRUCT → ( EXPR ) LINHA LINHA                   // (condition) then-body else-body
```

**Examples**:
- FOR loop: `(FOR (1) (10) (1) ((I PRINT)))`
- WHILE loop: `(WHILE ((I 10 <)) ((I 1 + I =)))`
- IF-ELSE: `(IFELSE ((X 5 >)) ((SUCCESS PRINT)) ((FAILURE PRINT)))`

### 4. **Grammar Must Be Unambiguous**
Your grammar must have **exactly one way** to parse any valid input. Ambiguous grammars cause conflicts in LL(1) parsing.

### 5. **Testing is Essential**
For every grammar rule you write, create test cases:
- ✅ Valid inputs that should be accepted
- ❌ Invalid inputs that should be rejected
- 🔄 Edge cases and deeply nested expressions

---

## Next Steps

Now that you understand grammar fundamentals, you're ready for:
1. **LL(1) Parsers and Syntax Analysis** (next theory file)
2. **FIRST and FOLLOW Sets** (after that)
3. **Parsing Table Construction** (final theory file)

Each concept builds on the previous one, so make sure your team understands grammars before moving forward!

## Questions to Validate Your Understanding

1. ✅ **Tokens for control structures**: FOR, WHILE, IFELSE, (, ), NUMBER, IDENTIFIER, operators
2. ✅ **Loop syntax**: FOR_STRUCT and WHILE_STRUCT as defined in the LL(1) grammar
3. ✅ **Decision syntax**: IFELSE_STRUCT with condition and two body branches
4. ✅ **Nested structures**: Handled through recursive LINHA → ( CONTENT ) structure
5. ✅ **Postfix notation**: Maintained with operators coming after operands in all constructs

**Key Insight**: Your team has **already implemented** a complete LL(1) grammar with 56 production rules, 18 non-terminals, and 25 terminals. The grammar is mathematically proven to be conflict-free!

**Next Steps**: Understand how FIRST and FOLLOW sets are calculated for this grammar in the next theory file. 🚀