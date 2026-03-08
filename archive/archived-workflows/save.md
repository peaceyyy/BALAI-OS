# /save — Mid-session checkpoint

---
description: Mid-session checkpoint
---
> **Use Case**: Save progress mid-session without closing. Resume immediately after.

## 1. Quick Session Log Update

- [ ] Identify current session log in `logs/sessions/` (or create if missing)
- [ ] Append checkpoint entry
- [ ] Format: Checkpoint entry with timestamp and bullet summary

```markdown
### Checkpoint [HH:MM SGT]

- [Brief summary of what was discussed/accomplished since last save]
- [Any key decisions or insights]
```

## 2. Resume

- [ ] Confirm: "📍 Checkpoint saved. Continuing session."
- [ ] Continue with user's next query

---

## What /save SKIPS (deferred to /end)

| Task                     | /save | /end |
| ------------------------ | ----- | ---- |
| Session log update       | ✅    | ✅   |
| Maintenance scripts      | ❌    | ✅   |
| Coherence check          | ❌    | ✅   |
| Cross-reference audit    | ❌    | ✅   |
| Git commit               | ❌    | ✅   |
| Profile/protocol updates | ❌    | ✅   |

---

## When to Use

- Long sessions with natural break points
- Before switching topics (preserve context)
- Before risky experiments (rollback point)
- "Save my progress, I'll be back"

---

## Tagging

#workflow #automation #save
