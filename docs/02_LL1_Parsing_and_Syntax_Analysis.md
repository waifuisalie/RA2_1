# LL(1) Parsing and Syntax Analysis: The Complete Guide

## Table of Contents
1. [What is LL(1) Parsing?](#what-is-ll1-parsing)
2. [Derivations and Parse Trees](#derivations-and-parse-trees)
3. [Grammar Ambiguity - The LL(1) Killer](#grammar-ambiguity---the-ll1-killer)
4. [Left Recursion Elimination](#left-recursion-elimination)
5. [NULLABLE, FIRST, and FOLLOW Sets](#nullable-first-and-follow-sets)
6. [Building the LL(1) Parsing Table](#building-the-ll1-parsing-table)
7. [The LL(1) Parsing Algorithm](#the-ll1-parsing-algorithm)
8. [Practical Examples](#practical-examples)
9. [Common Conflicts and Solutions](#common-conflicts-and-solutions)
10. [Key Takeaways for RA2](#key-takeaways-for-ra2)

## What is LL(1) Parsing?

### The Sherlock Holmes of Compilers
Think of an LL(1) parser as Sherlock Holmes examining a crime scene (your code). Just like Holmes, the parser must verify every detail against a known pattern (the grammar) to determine if the "evidence" (tokens) makes sense.

### What Does LL(1) Mean?
- **First L**: **Left-to-right** scan of input (reads tokens from left to right)
- **Second L**: **Leftmost** derivation (always expands the leftmost non-terminal first)
- **(1)**: Uses **1 symbol lookahead** (decides what to do by looking at just the next token)

### Key Characteristics
1. **Predictive**: Can predict which grammar rule to use without backtracking
2. **Deterministic**: Each step has exactly one choice - no ambiguity
3. **Top-Down**: Builds parse tree from root (start symbol) to leaves (terminals)
4. **Efficient**: Linear time complexity O(n)

### Why LL(1) for Your RPN Language?
Your RPN expressions like `((A B +) (C D *) /)` have perfect nested structure that LL(1) parsers handle beautifully!

## Derivations and Parse Trees

### What is a Derivation?
A **derivation** is the step-by-step process of generating a valid sentence from your grammar's start symbol.

#### Example: Simple Expression Grammar
```
E → T + E | T
T → F * T | F
F → (E) | id
```

### Leftmost vs Rightmost Derivations

For the input `id + id * id`:

#### **Leftmost Derivation** (what LL(1) uses):
```
E ⇒ T + E          // Expand leftmost E
  ⇒ F + E          // Expand leftmost T
  ⇒ id + E         // Expand leftmost F
  ⇒ id + T         // Expand leftmost E
  ⇒ id + F * T     // Expand leftmost T
  ⇒ id + id * T    // Expand leftmost F
  ⇒ id + id * F    // Expand leftmost T
  ⇒ id + id * id   // Expand leftmost F
```

#### **Rightmost Derivation**:
```
E ⇒ T + E          // Expand E
  ⇒ T + T          // Expand rightmost E
  ⇒ T + F * T      // Expand rightmost T
  ⇒ T + F * F      // Expand rightmost T
  ⇒ T + F * id     // Expand rightmost F
  ⇒ T + id * id    // Expand rightmost F
  ⇒ F + id * id    // Expand rightmost T
  ⇒ id + id * id   // Expand rightmost F
```

### Parse Trees: The Visual Structure

A **parse tree** shows the hierarchical structure of your parsed input. Both derivations above produce the same parse tree:

```
       E
      / \
     T   E
     |   |
     F   T
     |  /|\
    id F * T
       |   |
      id   F
           |
          id
```

**Key Insight**: Different derivation orders → Same parse tree structure!

## Grammar Ambiguity - The LL(1) Killer

### What Makes a Grammar Ambiguous?

A grammar is **ambiguous** if the same input string can produce **multiple different parse trees**. This is LL(1)'s worst enemy!

#### Example of Ambiguous Grammar:
```
E → E + E | E * E | id
```

For input `id + id * id`, this grammar can produce TWO different parse trees:

**Tree 1**: `(id + id) * id` - Addition first
```
     E
    /|\
   E * E
  /|\  |
 E + E id
 |   |
id  id
```

**Tree 2**: `id + (id * id)` - Multiplication first
```
     E
    /|\
   E + E
   |  /|\
  id E * E
     |   |
    id  id
```

### Why Ambiguity Breaks LL(1)

LL(1) parsers must make **deterministic decisions** with only 1 lookahead token. If a grammar is ambiguous:
- The parser can't decide which rule to apply
- This creates **conflicts** in the parsing table
- Your parser will fail or behave unpredictably

### Real Example from Your RPN Project

**Ambiguous** (DON'T do this):
```
EXPR → EXPR EXPR OP | NUMBER    // Left recursion + ambiguous
```

**Unambiguous** (DO this):
```
EXPR → (OPERAND OPERAND OPERATOR)    // Clear RPN structure
OPERAND → NUMBER | IDENTIFIER | EXPR
OPERATOR → + | - | * | / | % | ^ | |
```

## Left Recursion Elimination

### Why Left Recursion is LL(1)'s Kryptonite

**Left recursion** occurs when a non-terminal can derive itself as the first symbol:
```
A → Aα | β    // Direct left recursion
```

This causes **infinite loops** in LL(1) parsers because:
1. Parser sees non-terminal A
2. Tries to expand A using rule A → Aα
3. First symbol is still A, so tries to expand again
4. Loop continues forever!

### The Standard Elimination Technique

**Transform**: `A → Aα | β`
**Into**:
```
A → βA'
A' → αA' | ε
```

#### Example: Expression Grammar

**Before** (Left recursive):
```
E → E + T | T
T → T * F | F
F → (E) | id
```

**After** (LL(1) compatible):
```
E → TE'
E' → +TE' | ε
T → FT'
T' → *FT' | ε
F → (E) | id
```

### Why This Works
- Eliminates immediate self-reference
- Uses new non-terminal (A') to handle repetition
- ε (epsilon) allows the repetition to stop
- Maintains the same language recognition power

## NULLABLE, FIRST, and FOLLOW Sets

These three sets are the **mathematical foundation** of LL(1) parsing. Think of them as the "DNA" that determines if your grammar can work with LL(1).

### NULLABLE Set

**Definition**: Non-terminals that can derive the empty string (ε)

**Rules**:
1. If `A → ε` exists, then A is NULLABLE
2. If `A → B₁B₂...Bₙ` and ALL Bᵢ are NULLABLE, then A is NULLABLE

#### Example:
```
S → ABC
A → a | ε
B → CD
C → c | ε
D → A
```

**NULLABLE calculation**:
- A is NULLABLE (rule: A → ε)
- C is NULLABLE (rule: C → ε)
- D is NULLABLE (D → A, and A is NULLABLE)
- B is NULLABLE (B → CD, both C and D are NULLABLE)
- S is NULLABLE (S → ABC, all of A, B, C are NULLABLE)

**Result**: NULLABLE = {A, B, C, D, S}

### FIRST Set

**Definition**: FIRST(A) = all terminals that can start strings derived from A

**Rules**:
1. If A is terminal: FIRST(A) = {A}
2. For rule `A → Y₁Y₂...Yₙ`:
   - Add FIRST(Y₁) - {ε} to FIRST(A)
   - If Y₁ is NULLABLE, add FIRST(Y₂) - {ε} to FIRST(A)
   - Continue until you find non-NULLABLE symbol
   - If ALL symbols are NULLABLE, add ε to FIRST(A)

#### Example (using corrected expression grammar):
```
E → TE'
E' → +TE' | ε
T → FT'
T' → *FT' | ε
F → (E) | id
```

**FIRST calculation**:
- FIRST(F) = {(, id}
- FIRST(T') = {*, ε}
- FIRST(T) = FIRST(F) = {(, id}
- FIRST(E') = {+, ε}
- FIRST(E) = FIRST(T) = {(, id}

### FOLLOW Set

**Definition**: FOLLOW(A) = all terminals that can immediately follow A in some derivation

**FOLLOW Rules**:

**Rule 1**: Add $ to FOLLOW(start_symbol)

**Rule 2a**: For rule `B → αAβ`: Add FIRST(β) - {ε} to FOLLOW(A)

**Rule 2b**: For rule `B → αAβ`: If β is NULLABLE or β is empty, add FOLLOW(B) to FOLLOW(A)

#### CRITICAL: Understanding α, A, and β in Productions

**The pattern `B → αAβ` means**:
- **B**: The non-terminal on the LEFT side of the arrow
- **α** (alpha): ALL symbols that come BEFORE A in the production
- **A**: The specific non-terminal we're calculating FOLLOW for
- **β** (beta): ALL symbols that come AFTER A in the production

#### SUPER IMPORTANT: You Must Analyze EVERY Non-Terminal in Each Production!

**Key Insight**: For each production rule, you need to check **every non-terminal** that appears in the right-hand side separately. Each one gets its own α, A, β breakdown.

#### Let's Break Down α, A, β Step-by-Step

**Production: E' → +TE'**

This production contains **TWO non-terminals**: T and E'. We must analyze both!

**Scenario A: Analyzing T**
- **Full production**: E' → +TE'
- **We're looking at**: T (this is our A)
- **What comes BEFORE T**: + (this is α)
- **What comes AFTER T**: E' (this is β)
- **So**: B=E', α=+, A=T, β=E'
- **Apply Rule 2a**: Add FIRST(E') - {ε} to FOLLOW(T)
  - FIRST(E') = {+, ε}
  - FIRST(E') - {ε} = {+}
  - So add {+} to FOLLOW(T)
- **Apply Rule 2b**: Since ε ∈ FIRST(E'), add FOLLOW(E') to FOLLOW(T)
  - So add FOLLOW(E') to FOLLOW(T)

**Scenario B: Analyzing the second E'**
- **Full production**: E' → +TE'
- **We're looking at**: the second E' (this is our A)
- **What comes BEFORE the second E'**: +T (this is α)
- **What comes AFTER the second E'**: nothing (this is β = empty)
- **So**: B=E', α=+T, A=E', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(E') to FOLLOW(E')
  - This adds FOLLOW(E') to itself (no practical change)

**Key Point**: α can contain both terminals AND non-terminals! In scenario B, α=+T means "the terminal + and the non-terminal T both come before our target A."

#### More Examples of α, A, β Breakdown

**Production: T → FT'**

**Analyzing F**:
- **Full production**: T → FT'
- **Looking at**: F (this is A)
- **Before F**: nothing (α = empty)
- **After F**: T' (β = T')
- **So**: B=T, α=empty, A=F, β=T'
- **Apply Rule 2a**: Add FIRST(T') - {ε} to FOLLOW(F)
  - FIRST(T') = {*, ε}
  - FIRST(T') - {ε} = {*}
  - So add {*} to FOLLOW(F)
- **Apply Rule 2b**: Since ε ∈ FIRST(T'), add FOLLOW(T) to FOLLOW(F)
  - So add FOLLOW(T) to FOLLOW(F)

**Analyzing T'**:
- **Full production**: T → FT'
- **Looking at**: T' (this is A)
- **Before T'**: F (α = F)
- **After T'**: nothing (β = empty)
- **So**: B=T, α=F, A=T', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(T) to FOLLOW(T')
  - So add FOLLOW(T) to FOLLOW(T')

**Production: F → (E)**

**Analyzing E**:
- **Full production**: F → (E)
- **Looking at**: E (this is A)
- **Before E**: ( (α = ()
- **After E**: ) (β = ))
- **So**: B=F, α=(, A=E, β=)
- **Apply Rule 2a**: Add FIRST()) - {ε} to FOLLOW(E)
  - FIRST()) = {)}
  - FIRST()) - {ε} = {)} (since ) cannot derive ε)
  - So add {)} to FOLLOW(E)
- **Rule 2b doesn't apply**: β = ) is not empty and ) cannot derive ε

#### Complete FOLLOW Algorithm Process

For **every production rule**, you must:
1. **Scan through the right-hand side left to right**
2. **For each non-terminal you encounter**, set it as A
3. **Everything to the left becomes α**
4. **Everything to the right becomes β**
5. **Apply FOLLOW rules with that specific α, A, β**

#### Example: Complex Production Analysis

**Production: A → xyBzCwD** (where B, C, D are non-terminals; x, y, z, w are terminals)

You need **three separate analyses**:

**For B**: B=A, α=xy, A=B, β=zCwD
- **Apply Rule 2a**: Add FIRST(zCwD) - {ε} to FOLLOW(B)
- **Apply Rule 2b**: If ε ∈ FIRST(zCwD), add FOLLOW(A) to FOLLOW(B)

**For C**: B=A, α=xyBz, A=C, β=wD
- **Apply Rule 2a**: Add FIRST(wD) - {ε} to FOLLOW(C)
- **Apply Rule 2b**: If ε ∈ FIRST(wD), add FOLLOW(A) to FOLLOW(C)

**For D**: B=A, α=xyBzCw, A=D, β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(A) to FOLLOW(D)

#### Why This Matters

**EVERY non-terminal in a production can be followed by something different!**

In `E' → +TE'`:
- T can be followed by what E' can start with (because T is followed by E')
- The second E' can be followed by what the whole production E' can be followed by (because nothing comes after it)

This is why both scenarios A and B are **equally correct and necessary** for building complete FOLLOW sets!

#### Complete Step-by-Step FOLLOW Calculation with Rule Applications

Using this grammar:
```
E → TE'
E' → +TE' | ε
T → FT'
T' → *FT' | ε
F → (E) | id
```

**Step 1: Apply Rule 1**
- **Start symbol is E**
- **Apply Rule 1**: Add $ to FOLLOW(E)
- **Result**: FOLLOW(E) = {$}

**Step 2: Apply Rules 2a and 2b to each production**

**Production: E → TE'**

*Analyzing T*: B=E, α=empty, A=T, β=E'
- **Apply Rule 2a**: Add FIRST(E') - {ε} to FOLLOW(T)
  - FIRST(E') = {+, ε}
  - FIRST(E') - {ε} = {+}
  - Add {+} to FOLLOW(T)
- **Apply Rule 2b**: Since ε ∈ FIRST(E'), add FOLLOW(E) to FOLLOW(T)
  - Add FOLLOW(E) = {$} to FOLLOW(T)
- **Result**: FOLLOW(T) = {+, $}

*Analyzing E'*: B=E, α=T, A=E', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(E) to FOLLOW(E')
  - Add FOLLOW(E) = {$} to FOLLOW(E')
- **Result**: FOLLOW(E') = {$}

**Production: E' → +TE'**

*Analyzing T*: B=E', α=+, A=T, β=E'
- **Apply Rule 2a**: Add FIRST(E') - {ε} to FOLLOW(T)
  - FIRST(E') - {ε} = {+}
  - Add {+} to FOLLOW(T) (already there)
- **Apply Rule 2b**: Since ε ∈ FIRST(E'), add FOLLOW(E') to FOLLOW(T)
  - Add FOLLOW(E') = {$} to FOLLOW(T) (already there)
- **Result**: FOLLOW(T) = {+, $} (no change)

*Analyzing second E'*: B=E', α=+T, A=E', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(E') to FOLLOW(E')
  - No practical change

**Production: E' → ε**
- No non-terminals to analyze

**Production: T → FT'**

*Analyzing F*: B=T, α=empty, A=F, β=T'
- **Apply Rule 2a**: Add FIRST(T') - {ε} to FOLLOW(F)
  - FIRST(T') = {*, ε}
  - FIRST(T') - {ε} = {*}
  - Add {*} to FOLLOW(F)
- **Apply Rule 2b**: Since ε ∈ FIRST(T'), add FOLLOW(T) to FOLLOW(F)
  - Add FOLLOW(T) = {+, $} to FOLLOW(F)
- **Result**: FOLLOW(F) = {*, +, $}

*Analyzing T'*: B=T, α=F, A=T', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(T) to FOLLOW(T')
  - Add FOLLOW(T) = {+, $} to FOLLOW(T')
- **Result**: FOLLOW(T') = {+, $}

**Production: T' → *FT'**

*Analyzing F*: B=T', α=*, A=F, β=T'
- **Apply Rule 2a**: Add FIRST(T') - {ε} to FOLLOW(F)
  - Add {*} to FOLLOW(F) (already there)
- **Apply Rule 2b**: Since ε ∈ FIRST(T'), add FOLLOW(T') to FOLLOW(F)
  - Add FOLLOW(T') = {+, $} to FOLLOW(F) (already there)
- **Result**: FOLLOW(F) = {*, +, $} (no change)

*Analyzing second T'*: B=T', α=*F, A=T', β=empty
- **Apply Rule 2b**: Since β is empty, add FOLLOW(T') to FOLLOW(T')
  - No practical change

**Production: T' → ε**
- No non-terminals to analyze

**Production: F → (E)**

*Analyzing E*: B=F, α=(, A=E, β=)
- **Apply Rule 2a**: Add FIRST()) - {ε} to FOLLOW(E)
  - FIRST()) = {)}
  - Add {)} to FOLLOW(E)
- **Rule 2b doesn't apply**: ) cannot derive ε
- **Result**: FOLLOW(E) = {$, )}

**Production: F → id**
- No non-terminals to analyze

**Step 3: Update propagated changes**

Since FOLLOW(E) changed from {$} to {$, )}, we need to update:
- FOLLOW(E') gets FOLLOW(E) → FOLLOW(E') = {$, )}
- FOLLOW(T) gets FOLLOW(E) → FOLLOW(T) = {+, $, )}
- FOLLOW(T') gets FOLLOW(T) → FOLLOW(T') = {+, $, )}
- FOLLOW(F) gets FOLLOW(T) → FOLLOW(F) = {*, +, $, )}

**Final FOLLOW Sets**:
- FOLLOW(E) = {$, )}
- FOLLOW(E') = {$, )}
- FOLLOW(T) = {+, $, )}
- FOLLOW(T') = {+, $, )}
- FOLLOW(F) = {*, +, $, )}

## Building the LL(1) Parsing Table

The **parsing table** is your parser's "rulebook" - it tells the parser exactly which grammar rule to apply for each (non-terminal, terminal) combination.

### Table Construction Rules

For each production `A → α`:

1. **FIRST Rule**: For each terminal `a` in FIRST(α), add `A → α` to Table[A, a]
2. **FOLLOW Rule**: If ε ∈ FIRST(α), for each terminal `b` in FOLLOW(A), add `A → α` to Table[A, b]

### Example: Building the Table

Using our corrected expression grammar:

| Non-Terminal | id       | +        | *        | (        | )      | $ |
|--------------|----------|----------|----------|----------|--------|----|
| E            | E→TE'    |          |          | E→TE'    |        |    |
| E'           |          | E'→+TE'  |          |          | E'→ε   | E'→ε |
| T            | T→FT'    |          |          | T→FT'    |        |    |
| T'           |          | T'→ε     | T'→*FT'  |          | T'→ε   | T'→ε |
| F            | F→id     |          |          | F→(E)    |        |    |

### Detecting Conflicts

**No conflicts** = LL(1) grammar ✅
**Multiple entries in same cell** = Not LL(1) ❌

## The LL(1) Parsing Algorithm

### Core Components

1. **Stack**: Holds symbols being processed (starts with $ and start symbol)
2. **Input Buffer**: Contains tokens to be parsed (ends with $)
3. **Parsing Table**: Lookup table for decisions

### Algorithm Steps

```python
def ll1_parse(tokens, table):
    stack = ['$', 'START_SYMBOL']
    input_buffer = tokens + ['$']
    pointer = 0

    while len(stack) > 1:  # Until only $ remains
        top = stack[-1]
        current_token = input_buffer[pointer]

        if top == current_token:  # Terminal match
            stack.pop()
            pointer += 1
        elif top in NON_TERMINALS:  # Non-terminal
            if table[top][current_token] is not None:
                stack.pop()
                production = table[top][current_token]
                # Push production symbols in reverse order
                for symbol in reversed(production):
                    if symbol != 'ε':
                        stack.append(symbol)
            else:
                return "SYNTAX ERROR"
        else:
            return "SYNTAX ERROR"

    return "ACCEPT" if pointer == len(input_buffer) - 1 else "ERROR"
```

## Practical Examples

### Example: Parsing `id + id * id`

**Initial State**:
- Stack: ['$', 'E']
- Input: ['id', '+', 'id', '*', 'id', '$']

**Step-by-step trace**:

| Step | Stack              | Input         | Action               |
|------|-------------------|---------------|----------------------|
| 1    | ['$', 'E']        | id+id*id$     | E→TE' (Table[E,id])  |
| 2    | ['$', 'T', 'E'']  | id+id*id$     | T→FT' (Table[T,id])  |
| 3    | ['$', 'F', 'T'', 'E''] | id+id*id$ | F→id (Table[F,id])   |
| 4    | ['$', 'id', 'T'', 'E''] | id+id*id$ | Match id            |
| 5    | ['$', 'T'', 'E'']  | +id*id$      | T'→ε (Table[T',+])   |
| 6    | ['$', 'E'']        | +id*id$      | E'→+TE' (Table[E',+])|
| 7    | ['$', '+', 'T', 'E''] | +id*id$   | Match +              |
| 8    | ['$', 'T', 'E'']   | id*id$       | T→FT' (Table[T,id])  |
| ...  | ...               | ...          | ...                  |
| N    | ['$']             | $            | ACCEPT               |

## Common Conflicts and Solutions

### 1. FIRST/FIRST Conflicts

**Problem**: Two productions of same non-terminal have overlapping FIRST sets

**Example**:
```
A → aB | aC    // Both start with 'a' - conflict!
```

**Solution**: Left factoring
```
A → aA'
A' → B | C
```

### 2. FIRST/FOLLOW Conflicts

**Problem**: Production can derive ε and its FIRST overlaps with FOLLOW

**Example**:
```
A → Ba | ε
B → b
```
If 'a' ∈ FOLLOW(A), conflict occurs.

**Solution**: Grammar restructuring or using more powerful parser

### 3. Left Recursion

**Problem**: `A → Aα | β`

**Solution**: Standard elimination (as shown earlier)

## Key Takeaways for RA2

### 1. **Your RPN Grammar Design**
- **DO**: Use clear postfix structure: `EXPR → (OPERAND OPERAND OPERATOR)`
- **DON'T**: Create ambiguous rules or left recursion

### 2. **Control Structures in RPN**
Design unambiguous syntax like:
```
LOOP → (START_VALUE END_VALUE COUNTER FOR)
DECISION → (CONDITION IF THEN_EXPR ELSE ELSE_EXPR)
```

### 3. **Grammar Validation Checklist**
Before implementing:
- [ ] No left recursion
- [ ] No ambiguity
- [ ] FIRST/FOLLOW sets are disjoint
- [ ] All grammar rules handle RPN structure correctly

### 4. **Implementation Strategy**
1. **Start simple**: Basic RPN expressions only
2. **Test thoroughly**: Build FIRST/FOLLOW sets by hand first
3. **Add complexity gradually**: Add control structures after basic expressions work
4. **Validate table**: Check for conflicts before implementing parser

### 5. **Common Pitfalls to Avoid**
- **Mixing infix and postfix**: Stick to RPN throughout
- **Unclear precedence**: RPN eliminates this, but be consistent
- **Ambiguous control structures**: Design clear, unambiguous syntax

### 6. **Testing Strategy**
Create test cases covering:
- ✅ Simple RPN expressions: `(3 4 +)`
- ✅ Nested expressions: `((A B +) (C D *) /)`
- ✅ Control structures: `(1 10 I FOR)`
- ✅ Error cases: unbalanced parentheses, invalid operators
- ✅ Edge cases: empty expressions, single operands

---

## Next Steps

Now that you understand LL(1) parsing fundamentals:
1. **Next theory file**: FIRST and FOLLOW Set Calculation (detailed algorithms)
2. **After that**: LL(1) Table Construction and Conflict Resolution
3. **Finally**: Practical Implementation Guidelines for Your RPN Parser

Remember: **LL(1) parsing is deterministic by design**. If your grammar is well-designed and unambiguous, your parser will work perfectly! 🚀

## Questions for Team Discussion

1. How will you handle nested RPN expressions in your grammar?
2. What syntax will you use for loops: `(1 10 I FOR)` or something else?
3. What relational operators do you need: `>`, `<`, `==`, `!=`, `>=`, `<=`?
4. How will you test your grammar before implementing the parser?
5. What error recovery strategy will you use for invalid syntax?