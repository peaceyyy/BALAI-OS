# /think — Maximum reasoning depth

---
description: Maximum reasoning depth
---
> **Skill**: [reasoning-complex-logic](../skills/reasoning-complex-logic/SKILL.md)

## When to use

- You are stuck on a bug that makes no sense.
- You need to validate a high-stakes architectural decision.
- You want to break out of a "loop" of failed attempts.

## Workflow

### Step 0: Load Knowledge Sources

**REQUIRED:** Log all files being loaded for this workflow.

```bash
echo "📚 Loading knowledge sources for /think:"
echo "  - .agent/references/guidelines/115-first-principles-deconstruction.md"
echo "  - .agent/references/guidelines/137-graph-of-thoughts.md"
echo "  - .agent/references/guidelines/85-token-hygiene.md"
echo "  - .agent/references/guidelines/89-hybrid-token-conservation.md"
```

Verify files exist. If missing, log warning and proceed with degraded functionality.

1.  **Analyze**: The agent will use `sequential-thinking` to perform Root Cause Analysis.
2.  **Deconstruct**: If needed, it will break down the problem into First Principles.
3.  **Validate**: It will verify the hypothesis before coding.

## Related Protocols

- [First Principles](.agent/references/guidelines/115-first-principles-deconstruction.md)
- [Graph of Thoughts](.agent/references/guidelines/137-graph-of-thoughts.md)
- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md) - Monitor token budget during deep reasoning
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md) - Optimize agent selection

---

## References Used

This workflow relies on the following guidelines:

- [First Principles](.agent/references/guidelines/115-first-principles-deconstruction.md)
- [Graph of Thoughts](.agent/references/guidelines/137-graph-of-thoughts.md)
- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md)
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md)

_Note: These files are copied to your project during `/prime` or `boot_agent.py`._
