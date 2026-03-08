# BALAI OS — Script Reference Guide

This document explains how to call each script in `scripts/` from the terminal.

All commands should be run from the **project root** (the folder containing `.agent/`).

> [!IMPORTANT]
> These scripts sync files to your local IDE tools for **reference and exploration**. They do **not** auto-import or activate anything. Copilot, for example, surfaces synced files only when you manually reference them in a chat or invoke a slash command.

---

## Where Files End Up

The scripts push files to the following platform-specific locations on your machine.
Replace `<username>` with your Windows username (e.g. `Peace`).

| Content                    | Copilot Target Path                                                             |
| -------------------------- | ------------------------------------------------------------------------------- |
| Global Instructions        | `C:\Users\<username>\AppData\Roaming\Code\User\.github\copilot-instructions.md` |
| Workflows (Slash Commands) | `C:\Users\<username>\AppData\Roaming\Code\User\workflows\`                      |
| Personas (Prompts)         | `C:\Users\<username>\AppData\Roaming\Code\User\prompts\`                        |
| Skills                     | `C:\Users\<username>\.copilot\skills\`                                          |
| Protocols & References     | _(synced to a target folder of your choice — see below)_                        |

---

## Scripts

### `sync_global_rules.py`

Pushes `global_instructions.md` to your IDE global rules files.

```bash
# Push to both Antigravity (GEMINI.md) and Copilot (copilot-instructions.md)
python scripts/sync_global_rules.py

# Push to Copilot only
python scripts/sync_global_rules.py --copilot

# Push to Antigravity only
python scripts/sync_global_rules.py --antigravity
```

**What it writes:**

- `%USERPROFILE%\.gemini\GEMINI.md` (Antigravity)
- `%APPDATA%\Code\User\.github\copilot-instructions.md` (Copilot)

---

### `sync_workflows.py`

Pushes `.agent/workflows/*.md` to your IDE workflow directories.

```bash
# Push to both Antigravity and Copilot
python scripts/sync_workflows.py

# Push to Copilot only
python scripts/sync_workflows.py --copilot

# Push to Antigravity only
python scripts/sync_workflows.py --antigravity

# Force sync even if validation fails (missing description: field)
python scripts/sync_workflows.py --force
```

**What it writes:**

- `%APPDATA%\Code\User\workflows\<name>.prompt.md` (Copilot slash commands)
- `%USERPROFILE%\.gemini\antigravity\global_workflows\<name>.md` (Antigravity)

> [!NOTE]
> The script automatically rewrites frontmatter to match what each platform expects. Copilot gets `name`, `description`, and `argument-hint` (if previously set). Existing `argument-hint` values in Copilot target files are preserved on re-sync.

---

### `sync_skills.py`

Pushes the entire `.agent/skills/` folder (including all category subdirectories and `skill_index_*.md` files) to a target.

```bash
# Push to ~/.copilot/skills (skips references/)
python scripts/sync_skills.py --copilot

# Push to a custom directory
python scripts/sync_skills.py "C:\Path\To\Target"

# Force sync
python scripts/sync_skills.py --copilot --force
```

**What it writes to `~/.copilot/skills/`:**

```
skills/
  ├── core-engineering/
  ├── ui-ux-design/
  ├── devops-and-ops/
  ├── meta-agent-tools/
  ├── specialized-domains/
  ├── skill_index_kairou.md
  ├── skill_index_sparks.md
  ├── skill_index_arc.md
  ├── skill_index_janitor.md
  └── skill_index_secondary.md
```

---

### `sync_protocols.py`

Pushes `.agent/protocols/` (which contains both `guidelines/` and `references/`) to a target directory.

```bash
# Push to a custom directory (e.g. a project you're working in)
python scripts/sync_protocols.py "C:\Path\To\YourProject\.agent"

# Push to ~/.copilot (for Copilot reference access)
python scripts/sync_protocols.py --copilot

# Push to current working directory
python scripts/sync_protocols.py
```

**What it writes:**

```
protocols/
  ├── guidelines/            <- cognitive protocols 01-20 + guideline_index.md
  └── references/
        ├── llms.txt
        ├── learning_profile.md
        └── code-documentation/
```

---

## Typical Full Sync (First-Time Setup)

Run all scripts in sequence to push everything to Copilot at once:

```bash
python scripts/sync_global_rules.py --copilot
python scripts/sync_workflows.py --copilot
python scripts/sync_skills.py --copilot
```

Protocols are not pushed automatically to Copilot by default — they are bootstrapped into individual projects via `boot_agent.py` instead.

---

## Bootstrapping a New Project

`boot_agent.py` copies the entire `.agent/` folder into a target project root. This is the recommended way to initialize BALAI OS in a new workspace.

```bash
python boot_agent.py "C:\Path\To\YourProject"
```

This copies personas, skills, guidelines, references, workflows, templates, and global instructions into the target project's `.agent/` directory.
