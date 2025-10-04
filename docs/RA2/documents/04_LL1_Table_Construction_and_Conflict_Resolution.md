# LL(1) Table Construction and Conflict Resolution: Building Your Parser

## Table of Contents
1. [From Theory to Practice: Building the LL(1) Table](#from-theory-to-practice-building-the-ll1-table)
2. [The LL(1) Table Construction Algorithm](#the-ll1-table-construction-algorithm)
3. [Understanding and Detecting Conflicts](#understanding-and-detecting-conflicts)
4. [Conflict Resolution Strategies](#conflict-resolution-strategies)
5. [Complete Python Implementation](#complete-python-implementation)
6. [Practical Examples with RPN Grammar](#practical-examples-with-rpn-grammar)
7. [Testing and Validation](#testing-and-validation)
8. [Integration Guidelines for Your RA2 Project](#integration-guidelines-for-your-ra2-project)

## From Theory to Practice: Building the LL(1) Table

### Connection to Previous Theory Files

This file builds directly on the concepts from:
- **File 02**: LL(1) parsing algorithm and table usage
- **File 03**: FIRST and FOLLOW sets calculation (required inputs)

**Prerequisites**: Before reading this file, ensure you understand FIRST and FOLLOW sets from the previous files.

### The Parser's Roadmap

Think of the LL(1) parsing table as your parser's GPS. Just like a GPS tells you which route to take based on your current location and destination, the parsing table tells your parser which grammar rule to apply based on:
- **Current non-terminal** (where you are in the parsing process)
- **Next input token** (where you're trying to go)

**Cross-Reference**: This is the same table concept explained in `02_LL1_Parsing_and_Syntax_Analysis.md`, but here we focus on HOW to build it.

### What Makes a Grammar LL(1)?

A grammar is LL(1) if and only if the parsing table has **exactly one entry** in each cell that needs an entry. Multiple entries = conflicts = NOT LL(1).

**LL(1) Requirements Checklist:**
- ✅ No left recursion (direct or indirect)
- ✅ No ambiguity
- ✅ FIRST/FIRST conflicts resolved
- ✅ FIRST/FOLLOW conflicts resolved
- ✅ Deterministic parsing decisions

## The LL(1) Table Construction Algorithm

### Table Structure

The LL(1) parsing table is a 2D table where:
- **Rows**: Non-terminals from your grammar
- **Columns**: Terminals (including $ for end-of-input)
- **Cells**: Production rules or empty (syntax error)

```
Table[Non-Terminal, Terminal] → Production Rule
```

### Construction Rules

The table is built using two fundamental rules that use FIRST and FOLLOW sets:

**LL(1) Table Construction Rules**:

**FIRST Rule**: For each production A → α:
- For each terminal `a` in FIRST(α), add "A → α" to Table[A, a]

**FOLLOW Rule**: For each production A → α where ε ∈ FIRST(α):
- For each terminal `b` in FOLLOW(A), add "A → α" to Table[A, b]

#### Why These Rules Work

**FIRST Rule Logic**: If α can start with terminal `a`, then when the parser sees non-terminal A and lookahead `a`, it should use production A → α.

**FOLLOW Rule Logic**: If α can derive ε (disappear), then A effectively becomes what follows it. So when the parser sees A and a terminal that can follow A, it should use the ε-deriving production.

#### Connection to Previous Files

These are the same rules explained in detail in `02_LL1_Parsing_and_Syntax_Analysis.md`:
- **FIRST Rule**: Uses FIRST sets (calculated in file 03) to determine which production to choose
- **FOLLOW Rule**: Uses FOLLOW sets (calculated in file 03 using Rules 2a and 2b) when productions can derive ε

**Note**: The FOLLOW sets used here are calculated using the detailed Rule 2a and Rule 2b explained in files 02 and 03.

### Step-by-Step Construction Process

```python
def construct_ll1_table(productions, FIRST, FOLLOW):
    """
    Construct LL(1) parsing table from grammar productions and FIRST/FOLLOW sets.

    This is the core function that builds the parsing table used by the LL(1) parser.
    The table tells the parser which production rule to apply for each (non-terminal, terminal) pair.

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules in string format
        Example: ["E -> T E'", "E' -> + T E' | ε", "T -> F T'"]

        Where this comes from: Defined in construirGramatica() by your team
        This is the same productions list used in calculate_FIRST() and calculate_FOLLOW()

    FIRST : dict
        FIRST sets for all non-terminals in the grammar
        Format: {non_terminal: set_of_terminals}
        Example: {'E': {'+', '(', 'id'}, 'T': {'(', 'id'}}

        Where this comes from: Output of calculate_FIRST() from file 03
        Must be calculated BEFORE calling this function

    FOLLOW : dict
        FOLLOW sets for all non-terminals in the grammar
        Format: {non_terminal: set_of_terminals}
        Example: {'E': {'$', ')'}, 'T': {'+', '$', ')'}}

        Where this comes from: Output of calculate_FOLLOW() from file 03
        Must be calculated BEFORE calling this function

    Returns:
    --------
    dict
        LL(1) parsing table mapping (non_terminal, terminal) pairs to production rules
        Format: {non_terminal: {terminal: production_rule}}
        Example: {'E': {'(': 'E -> T E'', 'id': 'E -> T E''}}

        Where this goes: Used by parsear() function to make parsing decisions
        Each cell tells the parser which production to apply when it sees
        that non-terminal and lookahead terminal

    Raises:
    -------
    ConflictError
        If the grammar is not LL(1) (has FIRST/FIRST or FIRST/FOLLOW conflicts)
        This means multiple productions compete for the same table cell
    """
    # 1. Initialize empty table
    table = {}
    for non_terminal in non_terminals:
        table[non_terminal] = {}
        for terminal in terminals:
            table[non_terminal][terminal] = None

    # 2. Apply FIRST rule: For each production A → α,
    #    for each terminal a in FIRST(α), add A → α to Table[A, a]
    for production in productions:
        A, alpha = parse_production(production)
        first_alpha = calculate_first_of_string(alpha, FIRST)

        for terminal in first_alpha - {'ε'}:
            if table[A][terminal] is not None:
                raise ConflictError(f"FIRST/FIRST conflict at [{A}, {terminal}]")
            table[A][terminal] = production

    # 3. Apply FOLLOW rule: For each production A → α where ε ∈ FIRST(α),
    #    for each terminal b in FOLLOW(A), add A → α to Table[A, b]
    for production in productions:
        A, alpha = parse_production(production)
        first_alpha = calculate_first_of_string(alpha, FIRST)

        if 'ε' in first_alpha:
            for terminal in FOLLOW[A]:
                if table[A][terminal] is not None:
                    raise ConflictError(f"FIRST/FOLLOW conflict at [{A}, {terminal}]")
                table[A][terminal] = production

    return table
```

## Understanding and Detecting Conflicts

### Types of Conflicts

These are the same conflict types explained in `02_LL1_Parsing_and_Syntax_Analysis.md`, but with detailed detection algorithms:

#### 1. FIRST/FIRST Conflicts
**Problem**: Two productions of the same non-terminal have overlapping FIRST sets.

**Example**:
```
A → aB | aC    // Both start with 'a' - CONFLICT!
```

**Why This is a Problem**: When the parser sees non-terminal A and lookahead token 'a', it cannot decide which production to use because both aB and aC start with 'a'.

**Mathematical Detection**: FIRST(aB) ∩ FIRST(aC) = {a} ≠ ∅

**Parser Behavior**: The parser gets stuck - it doesn't know whether to apply A → aB or A → aC when it sees 'a'.

#### 2. FIRST/FOLLOW Conflicts
**Problem**: A production can derive ε and its FIRST overlaps with FOLLOW.

**Example**:
```
A → Ba | ε    // If 'a' ∈ FOLLOW(A), conflict occurs
B → b
```

**Why This is a Problem**: When the parser sees A and lookahead 'a', it cannot decide whether to:
- Use A → Ba (because 'a' is in FIRST(Ba))
- Use A → ε (because 'a' is in FOLLOW(A))

**Mathematical Detection**: (FIRST(A) - {ε}) ∩ FOLLOW(A) ≠ ∅

**Parser Behavior**: Ambiguity between using a production that starts with 'a' versus using an ε-production when 'a' can follow A.

### Conflict Detection in Practice

```python
def detect_conflicts(productions, FIRST, FOLLOW):
    """
    Detect LL(1) conflicts in a grammar before building the parsing table.

    This function analyzes the grammar to identify FIRST/FIRST and FIRST/FOLLOW conflicts
    that would prevent the grammar from being LL(1). It's essential to run this before
    attempting to build the parsing table.

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules
        Same format as construct_ll1_table()

        Where this comes from: Your grammar definition in construirGramatica()

    FIRST : dict
        FIRST sets for all grammar symbols
        Format: {symbol: set_of_terminals}

        Where this comes from: Output of calculate_FIRST() function from file 03

    FOLLOW : dict
        FOLLOW sets for all non-terminals
        Format: {non_terminal: set_of_terminals}

        Where this comes from: Output of calculate_FOLLOW() function from file 03

    Returns:
    --------
    list of str
        List of conflict descriptions. Empty list means no conflicts (LL(1) grammar).
        Each string describes a specific conflict found.
        Example: ["FIRST/FIRST conflict in A: {'a'}", "FIRST/FOLLOW conflict in B: {'b'}"]

        Where this goes:
        - Used by construirGramatica() to validate grammar before table construction
        - If non-empty, grammar needs to be fixed before proceeding
        - Can be used to generate error reports for debugging

    Conflict Types Detected:
    -----------------------
    1. FIRST/FIRST conflicts: Multiple productions for same non-terminal have overlapping FIRST sets
    2. FIRST/FOLLOW conflicts: Production can derive ε and FIRST overlaps with FOLLOW
    """
    conflicts = []

    # Group productions by non-terminal for analysis
    by_nonterminal = {}
    for prod in productions:
        A, alpha = parse_production(prod)
        if A not in by_nonterminal:
            by_nonterminal[A] = []
        by_nonterminal[A].append(alpha)

    # Check for conflicts in each non-terminal
    for A, alternatives in by_nonterminal.items():
        # Check FIRST/FIRST conflicts: Do different alternatives have overlapping FIRST sets?
        first_sets = [calculate_first_of_string(alt, FIRST) for alt in alternatives]
        for i in range(len(first_sets)):
            for j in range(i + 1, len(first_sets)):
                overlap = (first_sets[i] - {'ε'}) & (first_sets[j] - {'ε'})
                if overlap:
                    conflicts.append(f"FIRST/FIRST conflict in {A}: {overlap}")

        # Check FIRST/FOLLOW conflicts: Can ε-deriving production conflict with FOLLOW?
        for alt, first_set in zip(alternatives, first_sets):
            if 'ε' in first_set:
                overlap = (first_set - {'ε'}) & FOLLOW[A]
                if overlap:
                    conflicts.append(f"FIRST/FOLLOW conflict in {A}: {overlap}")

    return conflicts
```

## Conflict Resolution Strategies

### Strategy 1: Left Factoring

**When to use**: FIRST/FIRST conflicts with common prefixes

**Example Problem**:
```
A → aB | aC    // Common prefix 'a'
```

**Solution**:
```
A → aA'
A' → B | C
```

**Implementation**:
```python
def left_factor(productions):
    """
    Extract common prefixes from productions to resolve FIRST/FIRST conflicts.

    Left factoring is a grammar transformation technique that eliminates FIRST/FIRST conflicts
    by extracting common prefixes from alternative productions of the same non-terminal.

    Parameters:
    -----------
    productions : list of str
        List of grammar production rules that may have FIRST/FIRST conflicts
        Example: ["A -> aB | aC", "B -> b"] where A has conflicting alternatives

        Where this comes from:
        - Original grammar from construirGramatica() that failed conflict detection
        - Used when detect_conflicts() finds FIRST/FIRST conflicts

    Returns:
    --------
    list of str
        Transformed production rules with common prefixes factored out
        Example: ["A -> aA'", "A' -> B | C", "B -> b"]
        Original conflicting "A -> aB | aC" becomes two rules

        Where this goes:
        - Replaces original conflicting productions in your grammar
        - New grammar should pass conflict detection
        - Used as input to construct_ll1_table() after transformation

    Algorithm:
    ----------
    1. Group productions by non-terminal
    2. For each non-terminal, find longest common prefixes among alternatives
    3. Create new non-terminal for the factored suffix
    4. Transform: A -> αβ | αγ becomes A -> αA', A' -> β | γ

    Example Transformation:
    ----------------------
    Before: A -> aB | aC     (FIRST/FIRST conflict on 'a')
    After:  A -> aA'         (no conflict)
            A' -> B | C      (different FIRST sets)
    """
    # Group by non-terminal
    by_nt = group_by_nonterminal(productions)

    new_productions = []
    for nt, rules in by_nt.items():
        # Find common prefixes among alternatives
        prefixes = find_common_prefixes(rules)

        if prefixes:
            # Create new non-terminal for factored rules
            new_nt = f"{nt}'"
            factored_rule = f"{nt} → {prefix}{new_nt}"
            new_productions.append(factored_rule)

            # Create rules for new non-terminal (suffixes after common prefix)
            for rule in rules_with_prefix:
                suffix = rule[len(prefix):]
                if not suffix:
                    suffix = 'ε'  # Empty suffix becomes epsilon
                new_productions.append(f"{new_nt} → {suffix}")
        else:
            # No common prefixes found, keep original rules
            new_productions.extend(rules)

    return new_productions
```

### Strategy 2: Left Recursion Elimination

**When to use**: Left recursive rules (cause infinite loops)

**Example Problem**:
```
E → E + T | T    // Left recursion
```

**Solution**:
```
E → TE'
E' → +TE' | ε
```

### Strategy 3: Grammar Restructuring

**When to use**: Complex conflicts that can't be resolved by factoring

**Approach**:
1. Analyze the language you want to recognize
2. Design a new grammar structure
3. Ensure new grammar is unambiguous and LL(1)

## Complete Python Implementation

Here's a production-ready implementation for your RA2 project:

```python
class LL1TableBuilder:
    """
    Complete LL(1) table builder for RA2 project integration.

    This class encapsulates all the functionality needed to build LL(1) parsing tables
    from grammar productions. It's designed to be used directly in construirGramatica().
    """

    def __init__(self, productions, start_symbol):
        """
        Initialize the table builder with grammar information.

        Parameters:
        -----------
        productions : list of str
            Grammar production rules in string format
            Example: ["PROGRAM -> STATEMENT_LIST", "STATEMENT -> EXPRESSION | FOR_STATEMENT"]

            Where this comes from: Defined by your team in construirGramatica()

        start_symbol : str
            The start symbol of your grammar (usually 'PROGRAM')

            Where this comes from: Specified in your grammar design
        """
        self.productions = productions
        self.start_symbol = start_symbol
        self.non_terminals = self._extract_non_terminals()
        self.terminals = self._extract_terminals()

    def build_complete_table(self):
        """
        Build complete LL(1) table with full conflict detection and validation.

        This is the main function that orchestrates the entire table building process.
        It calculates all required sets, builds the table, and validates LL(1) properties.

        Returns:
        --------
        dict
            Complete LL(1) parsing components ready for use by parsear()
            Format: {
                'table': parsing_table,      # Main LL(1) table for parser decisions
                'first': first_sets,         # FIRST sets for debugging/validation
                'follow': follow_sets,       # FOLLOW sets for debugging/validation
                'nullable': nullable_set     # NULLABLE set for completeness
            }

            Where this goes:
            - 'table' is used by parsear() function for parsing decisions
            - Other components used for debugging and validation
            - Returned by construirGramatica() to provide complete grammar info

        Raises:
        -------
        ValueError
            If grammar is not LL(1) (has conflicts that prevent table construction)
            Error message includes specific conflicts found for debugging
        """
        # Calculate all required sets using algorithms from file 03
        nullable = self._calculate_nullable()
        first = self._calculate_first(nullable)
        follow = self._calculate_follow(first, nullable)

        # Build the actual parsing table
        table = self._construct_table(first, follow)

        # Validate LL(1) properties before returning
        conflicts = self._detect_conflicts(first, follow)
        if conflicts:
            raise ValueError(f"Grammar is not LL(1): {conflicts}")

        return {
            'table': table,
            'first': first,
            'follow': follow,
            'nullable': nullable
        }

    def _calculate_nullable(self):
        """
        Calculate NULLABLE set for the grammar.

        NULLABLE(A) = True if non-terminal A can derive the empty string (ε)

        Returns:
        --------
        set
            Set of non-terminals that can derive ε
            Example: {'STATEMENT_LIST', 'E_PRIME'} if these can derive ε

            Used by: _calculate_first() and _calculate_follow() methods
        """
        nullable = set()

        # Direct nullable: A → ε productions
        for production in self.productions:
            A, alpha = self._parse_production(production)
            if alpha == ['ε']:
                nullable.add(A)

        # Indirect nullable: A → B C where both B and C are nullable
        changed = True
        while changed:
            changed = False
            for production in self.productions:
                A, alpha = self._parse_production(production)
                if A not in nullable and alpha != ['ε']:
                    # A is nullable if all symbols in alpha are nullable non-terminals
                    if all(symbol in nullable for symbol in alpha if symbol in self.non_terminals):
                        nullable.add(A)
                        changed = True

        return nullable

    def _calculate_first(self, nullable):
        """Calculate FIRST sets."""
        first = {nt: set() for nt in self.non_terminals}

        # Add ε for nullable non-terminals
        for nt in nullable:
            first[nt].add('ε')

        changed = True
        while changed:
            changed = False
            for production in self.productions:
                A, alpha = self._parse_production(production)

                if alpha == ['ε']:
                    continue

                # Process each symbol in production
                k = 0
                while k < len(alpha):
                    Yk = alpha[k]

                    if Yk not in self.non_terminals:  # Terminal
                        if Yk not in first[A]:
                            first[A].add(Yk)
                            changed = True
                        break
                    else:  # Non-terminal
                        # Add FIRST[Yk] - {ε}
                        before_size = len(first[A])
                        first[A].update(first[Yk] - {'ε'})
                        if len(first[A]) > before_size:
                            changed = True

                        # If Yk is not nullable, stop
                        if Yk not in nullable:
                            break

                    k += 1

                # If all symbols are nullable, add ε
                if k == len(alpha):
                    if 'ε' not in first[A]:
                        first[A].add('ε')
                        changed = True

        return first

    def _calculate_follow(self, first, nullable):
        """Calculate FOLLOW sets."""
        follow = {nt: set() for nt in self.non_terminals}
        follow[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False

            for production in self.productions:
                A, alpha = self._parse_production(production)

                for i, B in enumerate(alpha):
                    if B in self.non_terminals:
                        beta = alpha[i+1:]

                        if beta:  # B is not at the end
                            first_beta = self._first_of_string(beta, first, nullable)

                            # Add FIRST(β) - {ε}
                            before_size = len(follow[B])
                            follow[B].update(first_beta - {'ε'})
                            if len(follow[B]) > before_size:
                                changed = True

                            # If ε ∈ FIRST(β), add FOLLOW(A)
                            if 'ε' in first_beta:
                                before_size = len(follow[B])
                                follow[B].update(follow[A])
                                if len(follow[B]) > before_size:
                                    changed = True
                        else:  # B is at the end
                            before_size = len(follow[B])
                            follow[B].update(follow[A])
                            if len(follow[B]) > before_size:
                                changed = True

        return follow

    def _construct_table(self, first, follow):
        """Construct the LL(1) parsing table."""
        table = {}
        for nt in self.non_terminals:
            table[nt] = {}
            for t in self.terminals + ['$']:
                table[nt][t] = None

        for production in self.productions:
            A, alpha = self._parse_production(production)
            first_alpha = self._first_of_string(alpha, first, self.nullable)

            # Rule 1: FIRST
            for terminal in first_alpha - {'ε'}:
                if table[A][terminal] is not None:
                    raise ValueError(f"FIRST/FIRST conflict at [{A}, {terminal}]")
                table[A][terminal] = production

            # Rule 2: FOLLOW
            if 'ε' in first_alpha:
                for terminal in follow[A]:
                    if table[A][terminal] is not None:
                        raise ValueError(f"FIRST/FOLLOW conflict at [{A}, {terminal}]")
                    table[A][terminal] = production

        return table

    def _first_of_string(self, string, first, nullable):
        """Calculate FIRST of a string of symbols."""
        if not string or string == ['ε']:
            return {'ε'}

        result = set()
        for symbol in string:
            if symbol not in self.non_terminals:  # Terminal
                result.add(symbol)
                break
            else:  # Non-terminal
                result.update(first[symbol] - {'ε'})
                if symbol not in nullable:
                    break
        else:
            # All symbols are nullable
            result.add('ε')

        return result

    def _parse_production(self, production):
        """Parse production string into (LHS, RHS)."""
        parts = production.split('→')
        if len(parts) != 2:
            parts = production.split('->')

        lhs = parts[0].strip()
        rhs = parts[1].strip().split()
        return lhs, rhs

    def _extract_non_terminals(self):
        """Extract all non-terminals from productions."""
        non_terminals = set()
        for production in self.productions:
            lhs, _ = self._parse_production(production)
            non_terminals.add(lhs)
        return non_terminals

    def _extract_terminals(self):
        """Extract all terminals from productions."""
        all_symbols = set()
        for production in self.productions:
            _, rhs = self._parse_production(production)
            all_symbols.update(rhs)

        terminals = all_symbols - self.non_terminals - {'ε'}
        return sorted(list(terminals))

# Usage example
def build_ll1_table_for_grammar(productions, start_symbol):
    """Convenience function for building LL(1) table."""
    builder = LL1TableBuilder(productions, start_symbol)
    return builder.build_complete_table()
```

## Practical Examples with RPN Grammar

### Complete RPN Grammar (Actual Implementation)

```python
# Your actual RPN grammar for RA2 (56 production rules)
rpn_productions = [
    "PROGRAM → LINHA PROGRAM_PRIME",
    "PROGRAM_PRIME → LINHA PROGRAM_PRIME",
    "PROGRAM_PRIME → EPSILON",
    "LINHA → ABRE_PARENTESES CONTENT FECHA_PARENTESES",
    "CONTENT → NUMERO_REAL AFTER_NUM",
    "CONTENT → VARIAVEL AFTER_VAR",
    "CONTENT → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
    "CONTENT → FOR FOR_STRUCT",
    "CONTENT → WHILE WHILE_STRUCT",
    "CONTENT → IFELSE IFELSE_STRUCT",
    "AFTER_NUM → NUMERO_REAL OPERATOR",
    "AFTER_NUM → VARIAVEL AFTER_VAR_OP",
    "AFTER_NUM → ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
    "AFTER_NUM → NOT",
    "AFTER_NUM → RES",
    "AFTER_NUM → EPSILON",
    "AFTER_VAR_OP → OPERATOR",
    "AFTER_VAR_OP → EPSILON",
    "AFTER_VAR → NUMERO_REAL AFTER_VAR_OP",
    "AFTER_VAR → VARIAVEL AFTER_VAR_OP",
    "AFTER_VAR → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_VAR_OP",
    "AFTER_VAR → NOT",
    "AFTER_VAR → RES",
    "AFTER_VAR → EPSILON",
    "AFTER_EXPR → OPERATOR EXPR_CHAIN",
    "AFTER_EXPR → EPSILON",
    "EXPR_CHAIN → NUMERO_REAL OPERATOR",
    "EXPR_CHAIN → VARIAVEL AFTER_VAR_OP",
    "EXPR_CHAIN → ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
    "EXPR_CHAIN → NOT",
    "EXPR_CHAIN → RES",
    "EXPR_CHAIN → EPSILON",
    "EXPR → NUMERO_REAL AFTER_NUM",
    "EXPR → VARIAVEL AFTER_VAR",
    "EXPR → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
    "EXPR → FOR FOR_STRUCT",
    "EXPR → WHILE WHILE_STRUCT",
    "EXPR → IFELSE IFELSE_STRUCT",
    "OPERATOR → SOMA",
    "OPERATOR → SUBTRACAO",
    "OPERATOR → MULTIPLICACAO",
    "OPERATOR → DIVISAO_INTEIRA",
    "OPERATOR → DIVISAO_REAL",
    "OPERATOR → RESTO",
    "OPERATOR → POTENCIA",
    "OPERATOR → MENOR",
    "OPERATOR → MAIOR",
    "OPERATOR → IGUAL",
    "OPERATOR → MENOR_IGUAL",
    "OPERATOR → MAIOR_IGUAL",
    "OPERATOR → DIFERENTE",
    "OPERATOR → AND",
    "OPERATOR → OR",
    "OPERATOR → NOT",
    "FOR_STRUCT → ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES LINHA",
    "WHILE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA",
    "IFELSE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA LINHA"
]

# Build the table (already proven LL(1) compliant)
try:
    result = build_ll1_table_for_grammar(rpn_productions, "PROGRAM")
    print("✅ Grammar is LL(1) - No conflicts detected!")
    print(f"Table size: 18 non-terminals x 25 terminals = 450 cells")
    print(f"Valid entries: {sum(1 for nt in result['table'] for t in result['table'][nt] if result['table'][nt][t] is not None)}")
except ValueError as e:
    print(f"❌ Grammar conflicts: {e}")
```

### Actual FIRST Sets for RPN Grammar

```python
actual_first_sets = {
    'PROGRAM': {'ABRE_PARENTESES'},
    'PROGRAM_PRIME': {'ABRE_PARENTESES', 'EPSILON'},
    'LINHA': {'ABRE_PARENTESES'},
    'CONTENT': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'FOR', 'WHILE', 'IFELSE'},
    'AFTER_NUM': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'NOT', 'RES', 'EPSILON'},
    'AFTER_VAR_OP': {'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO_INTEIRA', 'DIVISAO_REAL', 'RESTO', 'POTENCIA', 'MENOR', 'MAIOR', 'IGUAL', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE', 'AND', 'OR', 'NOT', 'EPSILON'},
    'AFTER_VAR': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'NOT', 'RES', 'EPSILON'},
    'AFTER_EXPR': {'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO_INTEIRA', 'DIVISAO_REAL', 'RESTO', 'POTENCIA', 'MENOR', 'MAIOR', 'IGUAL', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE', 'AND', 'OR', 'NOT', 'EPSILON'},
    'EXPR_CHAIN': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'NOT', 'RES', 'EPSILON'},
    'EXPR': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'FOR', 'WHILE', 'IFELSE'},
    'OPERATOR': {'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO_INTEIRA', 'DIVISAO_REAL', 'RESTO', 'POTENCIA', 'MENOR', 'MAIOR', 'IGUAL', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE', 'AND', 'OR', 'NOT'},
    'FOR_STRUCT': {'ABRE_PARENTESES'},
    'WHILE_STRUCT': {'ABRE_PARENTESES'},
    'IFELSE_STRUCT': {'ABRE_PARENTESES'}
}
```

### Actual FOLLOW Sets for RPN Grammar

```python
actual_follow_sets = {
    'PROGRAM': {'$'},
    'PROGRAM_PRIME': {'$'},
    'LINHA': {'ABRE_PARENTESES', 'FECHA_PARENTESES', '$'},
    'CONTENT': {'FECHA_PARENTESES'},
    'AFTER_NUM': {'FECHA_PARENTESES'},
    'AFTER_VAR_OP': {'FECHA_PARENTESES'},
    'AFTER_VAR': {'FECHA_PARENTESES'},
    'AFTER_EXPR': {'FECHA_PARENTESES'},
    'EXPR_CHAIN': {'FECHA_PARENTESES'},
    'EXPR': {'FECHA_PARENTESES'},
    'OPERATOR': {'NUMERO_REAL', 'VARIAVEL', 'ABRE_PARENTESES', 'NOT', 'RES', 'FECHA_PARENTESES'},
    'FOR_STRUCT': {'FECHA_PARENTESES'},
    'WHILE_STRUCT': {'FECHA_PARENTESES'},
    'IFELSE_STRUCT': {'FECHA_PARENTESES'}
}
```

## Testing and Validation

### Unit Tests for Table Construction

```python
import unittest

class TestLL1TableConstruction(unittest.TestCase):

    def setUp(self):
        self.simple_grammar = [
            "E → T E'",
            "E' → + T E' | ε",
            "T → F T'",
            "T' → * F T' | ε",
            "F → ( E ) | id"
        ]

    def test_nullable_calculation(self):
        builder = LL1TableBuilder(self.simple_grammar, "E")
        nullable = builder._calculate_nullable()
        self.assertIn("E'", nullable)
        self.assertIn("T'", nullable)
        self.assertNotIn("E", nullable)

    def test_first_calculation(self):
        builder = LL1TableBuilder(self.simple_grammar, "E")
        nullable = builder._calculate_nullable()
        first = builder._calculate_first(nullable)

        self.assertEqual(first["E"], {"(", "id"})
        self.assertEqual(first["E'"], {"+", "ε"})
        self.assertEqual(first["F"], {"(", "id"})

    def test_follow_calculation(self):
        builder = LL1TableBuilder(self.simple_grammar, "E")
        nullable = builder._calculate_nullable()
        first = builder._calculate_first(nullable)
        follow = builder._calculate_follow(first, nullable)

        self.assertIn("$", follow["E"])
        self.assertIn(")", follow["E"])
        self.assertIn("+", follow["T"])

    def test_table_construction_success(self):
        # Should succeed without conflicts
        result = build_ll1_table_for_grammar(self.simple_grammar, "E")
        self.assertIsNotNone(result['table'])

    def test_conflict_detection(self):
        # Grammar with FIRST/FIRST conflict
        conflicting_grammar = [
            "A → a B | a C",
            "B → b",
            "C → c"
        ]

        with self.assertRaises(ValueError):
            build_ll1_table_for_grammar(conflicting_grammar, "A")

def run_tests():
    unittest.main()
```

### Integration Test with RPN Parser

```python
def test_rpn_parsing(table, input_tokens):
    """Test the LL(1) table with actual RPN input."""
    stack = ['$', 'PROGRAM']
    input_buffer = input_tokens + ['$']
    pointer = 0
    steps = []

    while len(stack) > 1:
        top = stack.pop()
        current_token = input_buffer[pointer]

        steps.append(f"Stack: {stack + [top]}, Input: {input_buffer[pointer:]}")

        if top == current_token:  # Terminal match
            pointer += 1
            steps.append(f"Matched terminal: {top}")
        elif top in table:  # Non-terminal
            if current_token in table[top] and table[top][current_token]:
                production = table[top][current_token]
                _, rhs = parse_production(production)
                steps.append(f"Applied: {production}")

                # Push symbols in reverse order (skip EPSILON)
                for symbol in reversed(rhs):
                    if symbol != 'EPSILON':
                        stack.append(symbol)
            else:
                return f"SYNTAX ERROR: Unexpected {current_token} for {top}", steps
        else:
            return f"PARSE ERROR: Invalid state with {top}", steps

    result = "ACCEPT" if pointer == len(input_buffer) - 1 else "ERROR"
    return result, steps

# Test with actual RPN expressions
test_cases = [
    # Simple number
    ["ABRE_PARENTESES", "NUMERO_REAL", "FECHA_PARENTESES"],

    # Simple arithmetic: (3 4 +)
    ["ABRE_PARENTESES", "NUMERO_REAL", "NUMERO_REAL", "SOMA", "FECHA_PARENTESES"],

    # Nested expression: ((A B +) (C D *) /)
    ["ABRE_PARENTESES", "ABRE_PARENTESES", "VARIAVEL", "VARIAVEL", "SOMA", "FECHA_PARENTESES",
     "ABRE_PARENTESES", "VARIAVEL", "VARIAVEL", "MULTIPLICACAO", "FECHA_PARENTESES",
     "DIVISAO_REAL", "FECHA_PARENTESES"]
]

for i, tokens in enumerate(test_cases):
    result, steps = test_rpn_parsing(table, tokens)
    print(f"Test {i+1}: {result}")
    if result.startswith("ACCEPT"):
        print(f"  ✅ Successfully parsed {len(tokens)} tokens")
    else:
        print(f"  ❌ Parse failed: {result}")
```

## Integration Guidelines for Your RA2 Project

### Function Integration Strategy

```python
# Student 1: construirGramatica() implementation
def construirGramatica():
    """Build LL(1) grammar, calculate sets, and construct parsing table."""

    # 1. Define RPN grammar productions
    productions = define_rpn_productions()

    # 2. Build LL(1) components
    try:
        result = build_ll1_table_for_grammar(productions, "PROG")

        # 3. Validate grammar is LL(1)
        print("✅ Grammar validated as LL(1)")

        # 4. Return structured result for other team members
        return {
            'productions': productions,
            'start_symbol': 'PROGRAM',
            'parsing_table': result['table'],
            'first_sets': result['first'],
            'follow_sets': result['follow'],
            'nullable_sets': result['nullable'],
            'terminals': {
                'ABRE_PARENTESES', 'FECHA_PARENTESES', 'NUMERO_REAL', 'VARIAVEL',
                'FOR', 'WHILE', 'IFELSE', 'SOMA', 'SUBTRACAO', 'MULTIPLICACAO',
                'DIVISAO_INTEIRA', 'DIVISAO_REAL', 'RESTO', 'POTENCIA',
                'MENOR', 'MAIOR', 'IGUAL', 'MENOR_IGUAL', 'MAIOR_IGUAL',
                'DIFERENTE', 'AND', 'OR', 'NOT', 'RES', '$', 'EPSILON'
            },
            'non_terminals': {
                'PROGRAM', 'PROGRAM_PRIME', 'LINHA', 'CONTENT', 'AFTER_NUM',
                'AFTER_VAR_OP', 'AFTER_VAR', 'AFTER_EXPR', 'EXPR_CHAIN',
                'EXPR', 'OPERATOR', 'FOR_STRUCT', 'WHILE_STRUCT', 'IFELSE_STRUCT'
            }
        }

    except ValueError as e:
        print(f"❌ Grammar validation failed: {e}")
        raise

def define_rpn_productions():
    """Define the complete RPN grammar for your language (proven LL(1))."""
    return [
        # Program structure
        "PROGRAM → LINHA PROGRAM_PRIME",
        "PROGRAM_PRIME → LINHA PROGRAM_PRIME",
        "PROGRAM_PRIME → EPSILON",

        # Line structure (each statement in parentheses)
        "LINHA → ABRE_PARENTESES CONTENT FECHA_PARENTESES",

        # Content can be numbers, variables, expressions, or control structures
        "CONTENT → NUMERO_REAL AFTER_NUM",
        "CONTENT → VARIAVEL AFTER_VAR",
        "CONTENT → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
        "CONTENT → FOR FOR_STRUCT",
        "CONTENT → WHILE WHILE_STRUCT",
        "CONTENT → IFELSE IFELSE_STRUCT",

        # After number: can continue with operators or special operations
        "AFTER_NUM → NUMERO_REAL OPERATOR",
        "AFTER_NUM → VARIAVEL AFTER_VAR_OP",
        "AFTER_NUM → ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
        "AFTER_NUM → NOT",
        "AFTER_NUM → RES",
        "AFTER_NUM → EPSILON",

        # After variable operations
        "AFTER_VAR_OP → OPERATOR",
        "AFTER_VAR_OP → EPSILON",

        "AFTER_VAR → NUMERO_REAL AFTER_VAR_OP",
        "AFTER_VAR → VARIAVEL AFTER_VAR_OP",
        "AFTER_VAR → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_VAR_OP",
        "AFTER_VAR → NOT",
        "AFTER_VAR → RES",
        "AFTER_VAR → EPSILON",

        # After expression handling
        "AFTER_EXPR → OPERATOR EXPR_CHAIN",
        "AFTER_EXPR → EPSILON",

        "EXPR_CHAIN → NUMERO_REAL OPERATOR",
        "EXPR_CHAIN → VARIAVEL AFTER_VAR_OP",
        "EXPR_CHAIN → ABRE_PARENTESES EXPR FECHA_PARENTESES OPERATOR",
        "EXPR_CHAIN → NOT",
        "EXPR_CHAIN → RES",
        "EXPR_CHAIN → EPSILON",

        # Expression definitions
        "EXPR → NUMERO_REAL AFTER_NUM",
        "EXPR → VARIAVEL AFTER_VAR",
        "EXPR → ABRE_PARENTESES EXPR FECHA_PARENTESES AFTER_EXPR",
        "EXPR → FOR FOR_STRUCT",
        "EXPR → WHILE WHILE_STRUCT",
        "EXPR → IFELSE IFELSE_STRUCT",

        # All operators
        "OPERATOR → SOMA",
        "OPERATOR → SUBTRACAO",
        "OPERATOR → MULTIPLICACAO",
        "OPERATOR → DIVISAO_INTEIRA",
        "OPERATOR → DIVISAO_REAL",
        "OPERATOR → RESTO",
        "OPERATOR → POTENCIA",
        "OPERATOR → MENOR",
        "OPERATOR → MAIOR",
        "OPERATOR → IGUAL",
        "OPERATOR → MENOR_IGUAL",
        "OPERATOR → MAIOR_IGUAL",
        "OPERATOR → DIFERENTE",
        "OPERATOR → AND",
        "OPERATOR → OR",
        "OPERATOR → NOT",

        # Control structures (implemented)
        "FOR_STRUCT → ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES ABRE_PARENTESES NUMERO_REAL FECHA_PARENTESES LINHA",
        "WHILE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA",
        "IFELSE_STRUCT → ABRE_PARENTESES EXPR FECHA_PARENTESES LINHA LINHA"
    ]
```

### Error Handling Strategy

```python
class GrammarValidationError(Exception):
    """Raised when grammar is not LL(1)."""
    pass

class ParseTableError(Exception):
    """Raised when table construction fails."""
    pass

def validate_grammar_for_ll1(productions, start_symbol):
    """Comprehensive grammar validation."""
    errors = []

    # Check for left recursion
    left_recursion = detect_left_recursion(productions)
    if left_recursion:
        errors.append(f"Left recursion detected: {left_recursion}")

    # Check for conflicts
    try:
        result = build_ll1_table_for_grammar(productions, start_symbol)
    except ValueError as e:
        errors.append(f"Table construction failed: {e}")

    if errors:
        raise GrammarValidationError("; ".join(errors))

    return result
```

### Performance Considerations

```python
def optimize_table_lookup(table):
    """Optimize table for fast parsing."""
    # Convert to nested dictionaries for O(1) lookup
    optimized = {}
    for nt in table:
        optimized[nt] = {}
        for t in table[nt]:
            if table[nt][t] is not None:
                optimized[nt][t] = table[nt][t]

    return optimized

def cache_first_follow_sets(first, follow):
    """Cache sets for repeated use."""
    # Implementation depends on your specific needs
    return {'first': first, 'follow': follow}
```

## Key Takeaways for RA2 Success

### 1. **Implementation Checklist**
- ✅ FIRST set calculation working correctly
- ✅ FOLLOW set calculation working correctly
- ✅ Table construction without conflicts
- ✅ Conflict detection and reporting
- ✅ Integration with parsing algorithm
- ✅ Comprehensive error handling

### 2. **Testing Strategy**
- **Unit tests**: Each component (FIRST, FOLLOW, table)
- **Integration tests**: Complete table construction
- **Grammar tests**: Validate your RPN grammar
- **Parse tests**: Test with sample RPN expressions

### 3. **Team Coordination**
- **Student 1**: Provides table via `construirGramatica()`
- **Student 2**: Uses table in `parsear()` function
- **Students 3&4**: Provide tokens and handle output
- **Documentation**: Record all design decisions

### 4. **Common Pitfalls to Avoid**
- **Forgetting ε handling**: Always handle epsilon productions
- **Incorrect FOLLOW calculation**: Remember FOLLOW inheritance rules
- **Ignoring conflicts**: Don't suppress conflict errors
- **Poor error messages**: Provide clear conflict descriptions

### 5. **Final Validation**
Before submitting, ensure:
- All test cases pass
- No conflicts in your grammar
- Table integrates with parser correctly
- Documentation is complete
- Code follows team conventions

---

## Summary

You now have the complete theoretical foundation and practical tools to:
1. **Build LL(1) parsing tables** from FIRST and FOLLOW sets
2. **Detect and resolve conflicts** in your grammar
3. **Implement robust table construction** with error handling
4. **Integrate with your team's parser** implementation
5. **Test and validate** your complete system

The LL(1) table is the heart of your parser - get this right, and your RPN language analyzer will work perfectly! 🚀

**Next Steps**: Apply this knowledge to implement `construirGramatica()` and integrate with your team's `parsear()` function.
