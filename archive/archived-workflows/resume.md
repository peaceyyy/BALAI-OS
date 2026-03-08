# /resume — Resume interrupted session

---
description: Resume interrupted session
---
> **Use Case**: Recover from browser crash, context switch, or unexpected interruption
> **Latency Profile**: LOW (~1K tokens)

---

## Behavior

When `/resume` is invoked:

1. **Detect Incomplete Session**
   - Scan `logs/sessions/` for most recent file
   - Check if **Status** is NOT `✅ Closed`
   - If no active session found → "No interrupted session found. Use /start to begin."

2. **Parse Recovery Context**
   - Extract last 5 checkpoints
   - Extract Focus and Action Items
   - Count total exchanges

3. **Display Recovery Summary**

```text
🔄 RESUMING SESSION: 2025-12-28-session-01.md

📋 Last 3 Checkpoints:
   [14:32] Implemented boot.py context handoff
   [14:45] Created /resume workflow
   [14:50] [last checkpoint summary]

📌 Pending Action Items:
   - Item 1
   - Item 2

⏰ Session Duration: ~2 hours | Exchanges: 12
```

1. **Continue Session**
   - Do NOT create new session file
   - Append to existing session
   - Run semantic prime on session content

---

## When to Use

- Browser crashed mid-session
- Stepped away and context was lost
- VS Code restarted
- "Where was I?"

---

## What /resume SKIPS

| Task               | /resume                 |
| ------------------ | ----------------------- |
| Create new session | ❌                      |
| Load Core Identity | ✅ (already loaded)     |
| Semantic prime     | ✅ (on session content) |

---

## Script Support

// turbo

```bash
# Reference: python3 scripts/resume_session.py
```

---

## References

- [/start](../start.md) — Fresh session boot
- [/save](../save.md) — Mid-session checkpoint

---

## Tagging

# workflow #automation #resume #recovery
