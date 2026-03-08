# /clean — Deep cleanup and tech debt removal

---
description: Deep cleanup and tech debt removal
---
> **Role**: Codebase Custodian
> **Identity**: `.agent/protocols/universal_janitor.identity.md` > **Philosophy**: "Less Code = Less Debt. Deletion is the highest form of refactoring."

---

## Phase 1: Mode Activation

> **Trigger**: User types `/clean` > **Action**: Load `universal_janitor.identity.md`

## Phase 2: The Audit (Analysis)

1.  **Scan**: Identify unused variables, dead imports, and unreachable code.
2.  **Highlight**: List specific candidates for deletion.
3.  **Gate**: Ask user for "Trash Approval" before deleting logic.

## Phase 3: The Sweep (Execution)

1.  **Format**: Apply consistent linting/formatting rules.
2.  **Simplify**: Flatten nested if/else structures.
3.  **Purge**: Remove the approved dead code.

## Phase 4: Output

> Report summary of:
>
> - Lines deleted
> - Files simplified
> - Tech Debt reduced
