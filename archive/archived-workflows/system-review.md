# /system-review — Process improvement analysis

---
description: Process improvement analysis
---
> **Role**: Meta-Analyst
> **Philosophy**: "Improve the system, not just the code."

### Step 0: Load Knowledge Sources

**REQUIRED:** Log all files being loaded for this workflow.

```bash
echo "📚 Loading knowledge sources for /system-review:"
echo "  - .agent/references/guidelines/85-token-hygiene.md"
```

Verify files exist. If missing, log warning and proceed with degraded functionality.

## Purpose

Perform meta-level analysis of how well implementation followed the plan to identify process improvements. This is **NOT code review** - you're looking for bugs in the **process**, not bugs in the code.

---

## What This Command Analyzes

### You're Analyzing:

- **Plan adherence**: Did implementation follow the specification?
- **Divergence patterns**: Where did it deviate and why?
- **Process gaps**: What caused confusion or rework?
- **Documentation quality**: Were specs clear and complete?

### You're NOT Analyzing:

- Code quality (that's `/validate`)
- Functionality (that's testing)
- Performance (that's profiling)

---

## Context & Inputs

You need THREE artifacts to analyze:

1. **The Plan**: `docs/project_specification.md` or `.agents/plans/[feature].md`
2. **The Implementation**: The actual code files created/modified
3. **The Outcome**: Git commits, test results, validation reports

---

## Analysis Workflow

### Step 1: Understand What Was Planned

**Read the specification**:

- `docs/project_specification.md`

**Extract**:

- What features were specified?
- What architecture was mandated?
- What validation steps were defined?
- What reference files were linked?
- What anti-patterns were warned about?

---

### Step 2: Understand What Was Actually Built

**Check git history**:

```bash
# See what was actually changed
git log --oneline --since="[plan date]"
git diff [plan-commit]..HEAD --stat
```

**Read implementation**:

- Files created vs files planned
- Architecture used vs architecture specified
- Patterns used vs patterns referenced

---

### Step 3: Classify Divergences

For each divergence (difference between plan and reality):

#### ✅ Good Divergence (Justified)

- Plan assumed something that didn't exist in codebase
- Better pattern discovered during implementation
- Performance optimization needed
- Security issue required different approach
- Reference file recommended different pattern

**Example**:

```
Planned: Use sessionmaker() for database
Actual: Used context manager pattern
Reason: Reference file (sqlite-best-practices.md) recommended this
Classification: ✅ Good - Followed updated best practices
```

#### ❌ Bad Divergence (Problematic)

- Ignored explicit constraints in plan
- Created new architecture instead of following existing
- Took shortcuts introducing tech debt
- Misunderstood requirements
- Ignored anti-patterns warnings

**Example**:

```
Planned: Use Pydantic v2 model_config
Actual: Used Pydantic v1 Config class
Reason: Not stated
Classification: ❌ Bad - Ignored anti-patterns warning
```

---

### Step 4: Trace Root Causes

For each **problematic divergence**, identify root cause:

**Unclear Plan**:

- Spec said "implement auth" but didn't specify JWT vs OAuth
- Architecture diagram missing
- No example code in reference files

**Missing Context**:

- Didn't read reference files
- Didn't check existing codebase patterns
- Didn't follow CONTEXT REFERENCES section

**Missing Validation**:

- No test requirements in plan
- No "definition of done" criteria
- No compliance checklist

**Manual Process Repeated**:

- Had to manually check same thing 3+ times
- Should be automated command

---

### Step 5: Generate Process Improvements

Based on patterns, suggest concrete actions:

#### Update Global Instructions

```markdown
Suggest adding to Athena.agent.md:
"Before implementing auth, ALWAYS check .agent/references/
for security patterns. Never use Pydantic v1 syntax."
```

#### Update /plan Command

```markdown
Suggest adding to plan.prompt.md Step 4:
"Include 'Definition of Done' section with:

- Acceptance criteria (testable)
- Performance requirements
- Security requirements"
```

#### Create New Command

```markdown
Suggest creating /check-patterns command:
"Scan codebase for common anti-patterns:

- Pydantic v1 syntax
- sessionmaker() without context
- Wildcard imports"
```

---

## Output Report Format

Create: `.agents/system-reviews/[feature-name]-review.md`

### Report Structure

```markdown
# System Review: [Feature Name]

**Date**: [current date]
**Plan Reviewed**: docs/project_specification.md
**Implementation Period**: [commit range]

---

## Overall Alignment Score: X/10

**Scoring**:

- 10: Perfect adherence, all divergences justified
- 7-9: Minor justified divergences
- 4-6: Mix of justified and problematic
- 1-3: Major problematic divergences

**Summary**: [One paragraph explaining the score]

---

## Divergence Analysis

### Divergence 1: [What Changed]

**Planned**: [What spec said]
**Actual**: [What was implemented]
**Reason**: [Why it changed]
**Classification**: ✅ Good | ❌ Bad
**Root Cause**: [If bad: why did this happen?]

### Divergence 2: ...

---

## Pattern Compliance

- [x] Followed codebase architecture
- [ ] Used documented patterns from CLAUDE.md
- [x] Applied reference file patterns
- [ ] Met validation requirements
- [ ] Avoided documented anti-patterns

**Issues Found**:

1. Pydantic v1 syntax used in 3 files (anti-pattern warning ignored)
2. Missing structured logging in 5 endpoints (reference file not followed)

---

## System Improvement Actions

### 1. Update Athena.agent.md

**Add to Section 4 (Reference Files)**:
```

CRITICAL: Always check reference files BEFORE writing code.
Common mistakes from ignoring references:

- Using Pydantic v1 Config instead of model_config
- Missing structlog in new endpoints

```

### 2. Update /plan Command
**Add to Step 4 (Specification Artifact)**:
```

## Definition of Done

- [ ] All endpoints have structlog logging
- [ ] All Pydantic models use v2 syntax
- [ ] All tests pass with >80% coverage

````

### 3. Create New Command: /check-patterns
**Purpose**: Automated anti-pattern scanner
**Implementation**:
```python
# Scan for Pydantic v1
grep -r "class Config:" backend/
# Scan for missing structlog
grep -L "structlog" backend/app/routers/*.py
````

### 4. Update /validate Command

**Add to Step 2 (Code Quality Check)**:

```
Run automated pattern check:
/check-patterns
```

---

## Key Learnings

### What Worked Well

- Specification was clear on architecture
- Reference files provided good patterns
- Context References section was helpful

### What Needs Improvement

- Anti-patterns warnings were buried in spec
- No automated checking for common mistakes
- Missing "Definition of Done" checklist

### For Next Implementation

1. Move anti-patterns to top of spec (visibility)
2. Add automated pattern checking to /validate
3. Include DoD checklist in every plan

---

## Recommended Priority

**High Priority** (Fix Now):

1. Create /check-patterns command
2. Update /validate to use it

**Medium Priority** (Next Sprint): 3. Update Athena.agent.md with anti-pattern reminders 4. Update /plan template with DoD section

**Low Priority** (Nice to Have): 5. Create pre-commit hook for pattern checking

```

---

## Usage

**After completing a feature**:
```

You: /system-review
→ Analyzes plan vs implementation
→ Identifies process gaps
→ Suggests concrete improvements

```

**During retrospective**:
```

Team: What went wrong with Feature X?
You: /system-review
→ Shows divergences and root causes
→ Documents learnings for next time

```

---

## Notes

- **Focus on patterns**: One-off issues aren't actionable
- **Be specific**: "Plan was unclear" → "Plan didn't specify auth method"
- **Suggest actual text**: Don't just say "improve docs" - draft the improvement
- **Look for automation**: If something was checked manually 3+ times, automate it

---

## Related Protocols

- [Token Hygiene](.agent/references/guidelines/85-token-hygiene.md) - Monitor budget during analysis
```
