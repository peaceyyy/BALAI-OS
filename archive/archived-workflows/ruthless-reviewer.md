# /ruthless-reviewer — Security audit and vulnerability detection

---

## description: Security audit and vulnerability detection

> **Skill**: [securing-code](../skills/securing-code/SKILL.md)

## When to use

- You are about to deploy to production.
- You are adding authentication or payment logic.
- You want a security audit of your current changes.

### Step 0: Load Knowledge Sources

**REQUIRED:** Log all files being loaded for this workflow.

```bash
echo "📚 Loading knowledge sources for /ruthless-reviewer:"
echo "  - .agent/references/guidelines/85-token-hygiene.md"
echo "  - .agent/references/guidelines/87-container-sandboxing.md"
echo "  - .agent/references/guidelines/89-hybrid-token-conservation.md"
echo "  - .agent/skills/securing-code/vibe-security-checklist.md"
```

Verify files exist. If missing, log warning and proceed with degraded functionality.

## Workflow

1.  **Audit**: The agent analyzes code for security flaws (XSS, Injection, Leaks).
2.  **Block**: It will STOP you from committing if it finds hardcoded secrets (Token Hygiene).
3.  **Sanitize**: It suggests environment variable patterns.

## Related Protocols

- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md)
- [Container Sandboxing](.agent/references/guidelines/87-container-sandboxing.md)
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md)

---

## References Used

This workflow relies on the following guidelines:

- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md)
- [Container Sandboxing](.agent/references/guidelines/87-container-sandboxing.md)
- [Hybrid Token Conservation](.agent/references/guidelines/89-hybrid-token-conservation.md)

_Note: These files are copied to your project during `/prime` or `boot_agent.py`._
