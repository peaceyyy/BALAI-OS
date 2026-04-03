Summary: The invisible text issue occurs when automated dark mode extensions (like Dark Reader) fail to accurately guess your site's color pairs, typically because they invert a bright background while missing a hardcoded dark text color sitting on a transparent surface. This "orphaned color" problem, compounded by opacity and absolute layers, results in unreadable dark-on-dark contrast. To solve this natively, you should declare support via the color-scheme: light dark property—which signals extensions to back off—and adhere to a strict rule of never setting a text color without an explicit, variable-based background-color to ensure they always transition together as a readable unit.



🔍 Phase 1: Identifying Friction Points
Before modifying existing skills, audit the current interaction patterns for these "red flags":

Context Drift: The agent losing track of the core objective because the skill instructions are too long or noisy.
Boilerplate Redundancy: Identical rules (e.g., terminal command workarounds) appearing in multiple skill files.
Terminal Blindness: Workflows failing to account for system constraints like the cmd /c requirement or the "Phantom Quote" bug.
Vague Hand-offs: Workflow phases that lack clear "Success Criteria" or logical checkpoints for human review.
🛠️ Phase 2: Refinement Techniques
1. Atomic Skill Decomposition
If a skill handles more than 3 distinct responsibilities, it should be split into modular components.

Instead of: frontend-development-guide.md
Use Mono-responsibilities: styling-system.md, component-architecture.md, and api-hydration.md.
2. Prompt "Token Budgeting"
High-Density Instructions: Remove conversational filler from .md instructions. Use imperative, rule-based language.
YAML Frontmatter: Use metadata in skills to declare specific triggers and dependencies (e.g., requires: [git, node_js]).
3. Centralizing Workarounds
Ensure all logic-heavy workflows point back to a central System Constraint Skill.

Mandatory Pattern: Always use cmd /c [command] & REM \ for terminal calls.
Don't Guess: If an API or CLI tool is updated, immediately update the relevant skill to prevent the agent from using stale training data.
🚀 Phase 3: Workflow Orchestration
Refine your .agent/workflows/*.md files to be "Turbo-ready" for maximum efficiency:

Turbo-All Annotation: Use // turbo-all for battle-tested workflows where every step is safe to auto-run.
The "Measure Twice" Rule: Insert a mandatory view_file or grep_search step before any large-scale replace_file_content block to ensure target blocks match precisely.
Success Reporting: Every workflow should end with a "Task Handoff Report" that summarizes what was changed and what needs human validation.
✅ Phase 4: Validation Checklist
When adding or updating a skill/workflow, verify the following:

Deduplication: Does this rule already exist in global_instructions.md?
Persona Assignment: Is the correct persona (Kairou, Sparks, Arc, or Janitor) triggered by the workflow?
The "Glass Box" Principle: Does the skill force the agent to explain the "Mental Model" before writing code?
Resilience: Does the workflow survive a model switch (e.g., Gemini 3.1 Pro to Flash)?
📝 The Iteration Loop
Treat every session where an agent gets "stuck" or "loops" as valuable data. Update the relevant skill/workflow immediately after the issue is resolved to prevent that specific pattern of failure from recurring.