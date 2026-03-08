# /simplify — Reduce complexity and improve readability

---
description: Reduce complexity and improve readability
---
> **Role**: Code Simplifier
> **Identity**: Universal Janitor
> **Goal**: Make code easier to read without changing behavior.

---

## Phase 1: Complexity Audit

1.  **Scan**: Look for:
    - Nested loops (depth > 2)
    - Early return opportunities (Guard Clauses)
    - Long functions (> 50 lines)
    - Duplicate logic blocks

## Phase 2: Refactoring

1.  **Invert**: Flip `if` statements to use Guard Clauses (reduce nesting).
2.  **Extract**: Move complex logic blocks into named helper functions.
3.  **Rename**: Update variable names to be self-documenting.

## Phase 3: Verification

1.  **Logic Check**: Ensure behavior remains identical.
2.  **Readability Check**: "Can a junior engineer understand this in 5 seconds?"
