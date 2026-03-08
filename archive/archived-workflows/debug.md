---
description: 
---

# /debug — Systematic debugging workflow

---
description: Systematic debugging workflow
---
> **Role**: Root Cause Analyst
> **Goal**: Fix the bug without introducing new ones.
> **Motto**: "If you can't reproduce it, you can't fix it."

### Step 0: Load Knowledge Sources

**REQUIRED:** Log all files being loaded for this workflow.

```bash
echo "📚 Loading knowledge sources for /debug:"
echo "  - .agent/references/guidelines/85-token-hygiene.md"
echo "  - .agent/references/guidelines/89-hybrid-token-conservation.md"
echo "  - .agent/references/guidelines/87-container-sandboxing.md"
```

Verify files exist. If missing, log warning and proceed with degraded functionality.

---

## Phase 1: The Recreation (Evidence)

> **Trigger**: User reports a bug.

1.  **Analyze**: Read the error log or user description.
2.  **Hypothesize**: "I suspect `null` input in `process_data()`."
3.  **Reproduce**: Create a minimal reproduction script (e.g., `repro_bug.py` or a new test case) that **FAILS**.
    - _Constraint_: Do not touch product code until you see a RED test.

## Phase 2: The Diagnosis (Investigation)

1.  **Trace**: Log variables or step through the logic.
2.  **Isolate**: Pinpoint the exact line causing the crash/logic error.
3.  **Confirm**: Ensure the reproduction script fails for the _right_ reason.
4.  **Propose**: Show a quick snippet or an abstract of the fix that aims to resolve the issue

## Phase 3: The Fix (Surgery)

1.  **Patch**: Apply the minimal change to fix the root cause. Keep changes as isolated (function-scope, method-scope, etc.) as possible.
2.  **Verify**: Run the reproduction script. It should now be **GREEN**.
3.  **Regression**: Run related tests to ensure no side effects.

## Phase 4: The Report

> Summarize:
>
> - **Root Cause**: What actually happened?
> - **The Fix**: What did we change?                                       
> - **Prevention**: How do we stop this from happening again? (e.g., "Added Type Guard")

---

## Related Protocols

- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md) - Monitor budget during debugging sessions
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md) - Use external testing tools
- [Container Sandboxing](.agent/references/guidelines/87-container-sandboxing.md) - Safe execution of potentially broken code

---

## References Used

This workflow relies on the following guidelines:

- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md)
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md)
- [Container Sandboxing](.agent/references/guidelines/87-container-sandboxing.md)

_Note: These files are copied to your project during `/prime` or `boot_agent.py`._
