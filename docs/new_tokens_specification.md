# New Tokens Specification for RA2 - Control Structures and Relational Operators

## Overview

This document outlines the new tokens that need to be implemented for Phase 2 (RA2) of the compiler project, specifically for control structures (decision making and loops) and relational operators.

## PDF Requirements Summary

### What the PDF States

**Control Structures (Section 11.2.3, Page 4):**
> "Você deverá criar e documentar a sintaxe para estruturas de tomada de decisão e laços de repetição. A única restrição é que estas estruturas mantenham o padrão da linguagem: devem estar contidas entre parênteses e seguir a lógica de operadores pós-fixados."

**Relational Operators (Section 11.7.3, Page 8):**
> "Adicionar tokens para as estruturas de decisão e repetição e operadores relacionais (>, <, ==, etc.);"

**Test File Requirements (Section 11.4, Page 5):**
- Each test file must include at least one loop
- Each test file must include at least one decision structure

## Design Constraints

### Must Follow RPN Pattern
- All structures must be contained within parentheses `( )`
- Must follow postfix (RPN) notation logic
- Must maintain consistency with existing language patterns

### Existing Language Pattern Examples
```
(A B +)           # Addition: A + B
(A B *)           # Multiplication: A * B
(N RES)           # Get result from N lines back
(V MEM)           # Store V in memory MEM
(MEM)             # Retrieve value from MEM
```

## Required New Tokens

### 1. Relational Operators

Based on PDF specification, we need tokens for:

| Operator | Description | Usage Example |
|----------|-------------|---------------|
| `>` | Greater than | `(A B >)` → true if A > B |
| `<` | Less than | `(A B <)` → true if A < B |
| `==` | Equal to | `(A B ==)` → true if A == B |
| `>=` | Greater than or equal | `(A B >=)` → true if A >= B |
| `<=` | Less than or equal | `(A B <=)` → true if A <= B |
| `!=` | Not equal | `(A B !=)` → true if A != B |

### 2. Control Structure Tokens

#### Decision Making (IF structures)
**Proposed Token Design:**
- `IF` - Conditional execution token
- `ELSE` - Alternative execution token (optional)

**Syntax Proposals:**
```
# Simple IF: if condition then action
(condition action IF)

# IF-ELSE: if condition then action1 else action2  
(condition action1 action2 IFELSE)
```

#### Loop Structures
**Proposed Token Design:**
- `WHILE` - While loop token
- `FOR` - For loop token (if needed)
- `REPEAT` - Repeat/do-while token (alternative)

**Syntax Proposals:**
```
# WHILE loop: while condition do action
(condition action WHILE)

# FOR loop: for init condition increment action
(init condition increment action FOR)
```

### 3. Logical Operators (if needed)
| Operator | Description | Usage Example |
|----------|-------------|---------------|
| `AND` | Logical AND | `(cond1 cond2 AND)` |
| `OR` | Logical OR | `(cond1 cond2 OR)` |
| `NOT` | Logical NOT | `(condition NOT)` |

## Implementation Requirements

### Token Structure Integration
New tokens must integrate with existing token structure from RA1:
```python
Token: {
    'type': str,      # TokenType (RELATIONAL_OP, CONTROL_STRUCT, etc.)
    'value': str,     # Token value ('>', 'IF', 'WHILE', etc.)
    'line': int,      # Line number
    'column': int     # Column position
}
```

### Token Type Categories
- `RELATIONAL_OP` - For comparison operators (>, <, ==, etc.)
- `CONTROL_STRUCT` - For control flow keywords (IF, WHILE, etc.)
- `LOGICAL_OP` - For logical operators (AND, OR, NOT)

## Student Responsibilities

### Student 3 (lerTokens and Control Structures)
- Implement token recognition for new operators
- Define the exact syntax for control structures
- Create test cases with control structures
- Document the chosen syntax
- Ensure integration with Phase 1 token format

### Student 1 (Grammar Construction)
- Add grammar rules for new control structures
- Include new tokens in FIRST/FOLLOW calculations
- Update LL(1) parsing table with new productions

### Student 2 (Parser)
- Implement parsing logic for control structures
- Handle new token types in parsing functions
- Implement semantic validation for control flow

## Documentation Requirements

The team must create documentation including:

1. **Exact syntax specification** for each control structure
2. **Examples** of valid control structure usage
3. **Token definitions** and their meanings
4. **Grammar rules** in EBNF format
5. **Test cases** demonstrating all structures

## Examples to Design

The team needs to design syntax for scenarios like:

```
# Decision making example
if (A B >) then (A RESULT MEM) else (B RESULT MEM)

# Loop example  
while (COUNTER 10 <) do (COUNTER (COUNTER 1 +) MEM)

# Nested structures
if (X Y >) then 
    while (X 0 >) do (X (X 1 -) MEM)
else 
    (Y OUTPUT)
```

## Next Steps

1. **Team Meeting**: Decide on specific syntax for each control structure
2. **Prototype**: Create simple examples in chosen syntax
3. **Integration**: Ensure compatibility with existing RPN calculator
4. **Testing**: Create test files with various control structure combinations
5. **Documentation**: Write complete syntax specification

## Notes

- The PDF gives creative freedom in designing these structures
- Consistency with RPN postfix notation is mandatory
- All decisions must be documented for grading
- Integration with Phase 1 token format is critical
- Test files must demonstrate all implemented features