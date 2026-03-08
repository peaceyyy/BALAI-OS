# /validate — Implementation verification

---

## description: Implementation verification against spec and roadmap

> **Purpose**: "Definition of Done". Verify implementation meets spec, tests pass, and constitution is followed.
> **Output**: Validation Report (Pass/Fail).

## When to Use

- "I finished the feature"
- "Is this task done?"
- "Verify my implementation"

## Workflow

### Step 1: Check Functional Correctness

- **Compile**: `npm run build` / `compile`
- **Test**: `npm test` (or relevant suite)
- **Spec Check**: Does feature X exist as defined in `docs/project_specification.md`?

### Step 2: Check Constitution Compliance

**Read**: `.agent/personas/CONSTITUTION.md`
**Verify**:

- [ ] **SOLID**: Single Responsibility, Open/Closed, Liskov, Interface Seg, Dependency Inv.
- [ ] **DRY**: No blatant duplication.
- [ ] **KISS**: No over-engineering.
- [ ] **Test-First**: Do tests exist for the new code?

### Step 3: Check Documentation

- **Docs**: Are comments added? Is README updated?
- **Logs**: Is structured logging used?

### Step 4: Generate Report

```markdown
## ✅ Validation Report

**Feature**: [Feature Name]
**Spec**: [Spec Section]

### Functional (Pass)

- [x] Compilation
- [x] Unit Tests (12/12 passed)
- [x] API Endpoint Respond 200

### Constitution (Pass)

- [x] SOLID Principles met.
- [x] DRY met.
- [x] KISS met.

### Documentation (Pass)

- [x] Type definitions complete.
- [x] Comments present.

### Verdict: READY TO MERGE
```

---

## Related

- `/review-code` - To improve code quality before this step.
- `/commit` - To finalize the work if passed.
