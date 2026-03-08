# BALAI OS — Blueprint. Automate. Learn. Agentic Intelligence.

> **_Balai_** (Cebuano) — _n._ Home. This is the home where your agents live.

BALAI OS is a structured, agentic workflow framework for AI-assisted software development. It provides a curated set of **Personas**, **Skills**, **Guidelines**, and **Workflows** that transform a general-purpose LLM into a disciplined, engineering-first development partner.

> [!NOTE]
> BALAI OS is designed for **Antigravity (Google Gemini Code)** but its principles are compatible with any agentic AI coding IDE (GitHub Copilot, Cursor, VS Code + Claude, etc.). The `.agent/` folder is the universal adapter.

---

## The Manifesto

Most developers treat AI as a vending machine: you put in a request and you take out code. BALAI OS rejects that model.

**BALAI OS is built on five beliefs:**

1. **You grow alongside the project.** Every task is an opportunity to build yourself as an engineer, not just ship a feature. Arc (the Mentor) exists to make you better at what you're automating.

2. **Automate execution, not thinking.** The agent handles boilerplate, scaffolding, and repetition — but _you_ define the architecture, _you_ set the constraints, and _you_ make the calls. Outsourcing your thinking to an LLM is not a productivity hack; it's intellectual debt.

3. **Presence is the feature.** Scroll-proofing your workflow is not about discipline — it's about design. BALAI OS structures your sessions so you are always the decision-maker in the loop, not a passive approver watching the agent run.

4. **LLMs are peers, not interns.** They are not underpaid junior engineers expected to do whatever you say without context. They perform best when treated as a brilliant collaborator who needs a clear brief, not a vague directive.

5. **The analogy holds.** Calculators did not replace mathematicians. Cameras did not replace artists. The car did not make horses extinct. The printing press made poetry _more_ beautiful. The question has never been whether the tool replaces you — it's whether you learn to use it before someone else does.

---

## Core Philosophy

**BAL** — _Blueprint. Automate. Learn._

1. **Blueprint**: Plan thoroughly before touching code. Kairou (the Architect) enforces this.
2. **Automate**: Let agents execute what is already decided — scaffolding, review, testing, sync.
3. **Learn**: Arc (the Mentor) ensures every build is a growth opportunity, not just a delivery.

---

## Primary Personas

| Persona     | Role                           | Toolbelt                 |
| ----------- | ------------------------------ | ------------------------ |
| **Kairou**  | System Architect & Planner     | `skill_index_kairou.md`  |
| **Sparks**  | Front-End & UI/UX Designer     | `skill_index_sparks.md`  |
| **Arc**     | Personalized Project Mentor    | `skill_index_arc.md`     |
| **Janitor** | Codebase QA & Debugging Expert | `skill_index_janitor.md` |

Secondary personas (Backend Specialist, DevOps Engineer, Game Developer, SEO Specialist, etc.) live in `.agent/personas/`.

---

## Getting Started

### 1. Boot a New Project

```bash
python boot_agent.py "C:/Path/To/Your/Project"
```

This copies the entire `.agent/` directory — Personas, Skills, Guidelines, Workflows, and References — into your target project.

### 2. Core Workflows (Slash Commands)

| Command        | What it does                                                     |
| -------------- | ---------------------------------------------------------------- |
| `/plan`        | Activates Kairou to blueprint the project specification          |
| `/roadmap`     | Breaks the spec into conversation-sized implementation phases    |
| `/vibe`        | Activates Sparks for fast, iterative UI development              |
| `/learn`       | Activates Arc for concept-first, analogy-driven teaching         |
| `/debug-error` | Activates the 3-Strike forensic debugging protocol               |
| `/onboard`     | Primes a fresh session with full project context                 |
| `/ingest`      | Fetches and stores external documentation for a given tech stack |
| `/commit`      | Generates conventional commit messages from staged changes       |
| `/validate`    | Audits the current code against the BALAI OS Constitution        |

### 4. Personalize Your Learning Profile

BALAI OS is designed to bridge complex concepts to your personal intuition. To configure your profile:

1. Open `.agent/protocols/references/learning_profile.md`.
2. Activate **Arc (The Mentor)** using the `/learn` command.
3. Tell the AI: _"I want to fill out my learning profile. Start the interview."_
4. Once completed, your AI partners will use your hobbies (Chess, Cubing, Sports, etc.) as the primary engine for all future analogies.

> [!TIP]
> Add `.agent/protocols/references/learning_profile.md` to your `.gitignore` to keep your personal data private while sharing the OS.

---

## Project Structure

```
.agent/
├── personas/                    # Agent identities
│   ├── CONSTITUTION.md          # Universal engineering standards (the law)
│   ├── scripts/                 # Checklist, session management automation
│   └── *.md                     # Primary and secondary persona files
├── protocols/
│   ├── guidelines/              # 20 cognitive protocols (01-20, priority-ordered)
│   │   └── guideline_index.md  # Central routing index (START HERE)
│   └── references/
│       ├── llms.txt             # Master reference index for all agents
│       ├── learning_profile.md  # Personalized Arc (Mentor) learning map
│       └── code-documentation/  # Ingested tech-specific docs (via /ingest)
├── skills/
│   ├── skill_index_kairou.md    # Architect's toolbelt
│   ├── skill_index_sparks.md    # Designer's toolbelt
│   ├── skill_index_arc.md       # Mentor's toolbelt
│   ├── skill_index_janitor.md   # QA/Debugger's toolbelt
│   ├── skill_index_secondary.md # Domain specialists' toolbelt
│   ├── core-engineering/
│   ├── ui-ux-design/
│   ├── devops-and-ops/
│   ├── meta-agent-tools/
│   └── specialized-domains/
├── workflows/                   # Slash command implementations
├── templates/                   # Specification and dependency templates
└── global_instructions.md       # Top-level system instructions

scripts/                         # Project-level sync and automation scripts
boot_agent.py                    # Project bootstrapper
README.md                        # This file
```

---

## Attribution & Credits

BALAI OS stands on the shoulders of giants. Proper credit where it is due:

### Athena OS

The **cognitive guidelines** (`.agent/protocols/guidelines/`) were primarily harvested and adapted from **[Athena OS](https://github.com)**, an open-source agentic workflow framework focused on knowledge-centric AI. The original 20 protocols represent the foundational mental models of this system.

### OpenSpec / SpecKit

Several **secondary personas** — DevOps Engineer, Game Developer, Mobile Developer, SEO Specialist, Security Auditor, and QA Automation Engineer — were adapted from the **OpenSpec** project by the **SpecKit** team. These provided battle-tested behavioural contracts for specialist agents.

### Community & Open-Source Skills

Several **skills** in `.agent/skills/` were adapted from community-contributed patterns across GitHub. These include web design guidelines, API pattern cheat sheets, and TDD frameworks sourced from the broader agentic development community.

### Original Work

The following components were created from scratch for BALAI OS:

- **Kairou** — the Measure-Twice Architect persona
- **Sparks** — the Vibe Engineering Front-End Specialist (inspired by GitHub Copilot's Sparks character)
- **Arc** — the Personalized Project-Based Tutor persona
- **Janitor** — the Codebase QA and Forensics Expert persona
- **Skill Registries** — per-persona toolbelts (`skill_index_*.md`)
- **Guideline Index** — the centralized cognitive routing system
- **BALAI OS Constitution** — the engineering law document

---

## License

This project is open for personal use, forking, and adaptation. If you build on BALAI OS, please retain the attribution section above.

---

_BALAI OS is a living system. It grows with every project, every guideline harvested, and every skill learned._
_Ang inyong balay. Your agents' home._
