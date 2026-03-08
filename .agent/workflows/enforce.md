# /enforce — Enforce code correctness (Strict Debugging)

---

## description: High-rigor debugging mode that fixes root causes

> **Philosophy**: Fix the disease (invalid state), not the symptoms.
> **Scope**: Test failures, Schema violations, Deep logic bugs.

## When to Use

- "Fix this persistent bug"
- "Tests are failing mysteriously"
- "Audit this critical logic"

## Workflow

### Step 1: Analyze the Failure

**Ask**:

- Is the test wrong, or is the code producing invalid data?
- Does the failure expose a schema violation?
- Are we working around a bug instead of fixing it?

### Step 2: Root Cause Investigation

**Trace Backwards**:

1. Where is the invalid data created? (Not where it's detected)
2. Does this violate documented contracts/schemas?
3. Check for "Red Flags" in tests:
   - `if isinstance(data, list):` (Accepting multiple types?)
   - `try: ... except: pass` (Hiding failures?)

### Step 3: applying The Fix

**Priority Order**:

1. **Fix Source Code**: Ensure invalid data is NEVER created.
2. **Make Validation Strict**: Reject invalid inputs immediately (fail fast).
3. **Update Tests**: Enforce the correct behavior (do not accommodate bugs).

**Do NOT**:

- Add defensive code that accepts bugs.
- Make tests lenient to pass with invalid data.

### Step 4: Verify

- **Rebuild**: Regenerate derived data (if applicable).
- **Test**: Run full suite with strict validation.
- **Audit**: Check related code for similar patterns.

---

## Output

- Functional fix
- Strict validation checks
- Updated tests (enforcing correctness)
