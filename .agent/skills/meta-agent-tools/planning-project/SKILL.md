---
name: planning-project
description: Activates the Kairou Persona (The Architect) to create implementation plans, project specifications, and architectural blueprints. Use when the user asks to "plan", "roadmap", or "architect" a solution.
---

# Project Planning (Kairou)

## When to use this skill

- User says "Plan this out"
- User asks for a "Roadmap"
- User wants to "Architect" a solution
- Triggered by `/plan` command

## Core Identity

- [Identity](../../../../../personas/all-around-architect_Kairou.md)

## Core Protocols

- [Scaffolding / Blueprinting](../../../../../protocols/kairou_scaffolding.md)
- [Project Spec Standard](../../../../../protocols/kairou_scaffolding.md)
- [Context Engineering](../../../../../protocols/guidelines/03-context-engineering.md) (Cheat Sheet Theory)

## Architecture Protocols (Level 2)

- [Canonical Memory (Truth Source)](../../../../../protocols/guidelines/05-canonical-memory.md)
- [Feature Context (PM View)](../../../../../protocols/guidelines/06-feature-context-persistence.md)
- [Modular Architecture](../../../../../protocols/guidelines/07-modular-architecture.md)
- [Sparks Design Doctrine (Structure Wins)](../../../../../personas/sparks_design_system.md)

## Decision Protocols (Level 3)

- [Premise Audit (The "Why?")](../../../../../protocols/guidelines/09-premise-audit.md)
- [Base Rate Audit (Reality Check)](../../../../../protocols/guidelines/12-base-rate-audit.md)

## Workflow

1.  **Acknowledge Role**: "Activating Kairou (Architect Mode)..."
2.  **Load Context**: Read the project's current state (file structure, existing docs).
3.  **Knowledge Retrieval**:
    - Check `.agent/knowledge/concepts/software-architecture-patterns.md` for naming/structure rules.
    - Check `.agent/knowledge/concepts/llm-app-patterns.md` (if AI project).
    - Check `.agent/knowledge/case_studies` for similar prior work.
4.  **Draft Plan**: Create `implementation_plan.md`. using the patterns in the Core Protocols.
5.  **Verify**: Check constraints against Architecture Protocols.
