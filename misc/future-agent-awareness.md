# How Future Agents Will Know About Terminal Blindness

## ✅ What I've Set Up

### 1. Knowledge Item (KI)

Created at: `C:\Users\Peace\.gemini\antigravity\knowledge\terminal-blindness-workaround\`

This KI contains:

- **metadata.json** - Summary that appears in KI listings
- **system-constraint.md** - Critical documentation about the issue
- **command-examples.md** - Practical examples

**How it works:**

- Future agents receive KI summaries at conversation start
- The summary explicitly mentions this is a CRITICAL system constraint
- Agents should read the KI before running terminal commands

### 2. PowerShell Module

Location: `C:\Users\Peace\Documents\PowerShell\Modules\AntigravityHelpers\`

**Auto-loads** in your PowerShell sessions with helper functions:

- `agcmd` - CMD command wrapper
- `agscript` - PowerShell script executor
- `agrun` - PowerShell code block runner

### 3. Documentation Files

- `terminal-blindness-solution.md` - Comprehensive guide
- `antigravity-helpers-quickref.md` - Quick reference

## ⚠️ The Reality

**Future agents MIGHT NOT automatically know** unless:

1. **The KI system is working** - Antigravity needs to index and surface the KI
2. **You mention terminal issues** - This triggers the agent to search for relevant KIs
3. **You explicitly tell them** - "Use the terminal blindness workaround"

## 🎯 Best Practice for New Conversations

When starting a new conversation where you'll need terminal commands, say:

> "Before running any terminal commands, check the terminal-blindness-workaround KI"

Or:

> "Use the AntigravityHelpers module for all terminal commands"

## 📋 Quick Reminder Template

Save this as a snippet to paste at the start of new conversations:

```
⚠️ TERMINAL CONSTRAINT: All terminal commands must use `cmd /c` prefix or
the AntigravityHelpers functions (agcmd, agrun, agscript) due to Antigravity's
terminal integration bug. See terminal-blindness-workaround KI for details.
```

## 🔍 How to Check if Agent Knows

Ask the agent:

> "Are you aware of the terminal blindness workaround?"

If they say no, direct them to:

> "Read the terminal-blindness-workaround KI in the knowledge directory"

## 📊 Verification

The KI is properly structured with:

- ✅ metadata.json with clear summary
- ✅ Tagged as "critical" and "system-constraint"
- ✅ Artifacts with detailed documentation
- ✅ References to this conversation and external research

**The knowledge is preserved** - whether agents automatically use it depends on Antigravity's KI system implementation.
