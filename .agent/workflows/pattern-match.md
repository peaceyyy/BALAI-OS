# /pattern-match — External pattern extraction

---

## description: Analyze external patterns for internal integration

> **Purpose**: "Steal" good ideas. External Analysis -> Internal Pattern.
> **Output**: Reusable template/snippet, or design pattern docs.

## When to Use

- "Check how [Project X] does authentication"
- "Adapt the [feature] from [Repo Y]"
- "Extract this UI pattern"

## Workflow

### Step 1: Analyze External Source

- **Identify**: Target repo, documentation, or code snippet.
- **Deconstruct**: How does it work? (Architecture, State, API).
- **Abstract**: Remove implementation details to find the core pattern.

### Step 2: Contextualize Internal Needs

- **Map**: Relate external pattern to internal constraints.
- **Adapt**: Modify for existing codebase (e.g., Change strict types to interface).
- **Verify**: Does it fit our constitution (SOLID/DRY)?

### Step 3: Extract Pattern

- **Standardize**: Create a generic template/snippet.
- **Document**: Describe usage, pros/cons, and context.
- **Store**: Add to `.agent/knowledge/patterns/` or create a new template.

### Step 4: Apply Pattern (Optional)

- **Implement**: Apply the extracted pattern to the target file.
- **Verify**: Ensure it functions correctly in the new context.

---

## Output Format

```markdown
## 🧩 Pattern Extraction Report

**Source**: [External Source]
**Pattern Name**: [Name] (e.g., Result Pattern, Repository Pattern)

### Abstracted Plan

1. **Define Interface**: `IRepository<T>`
2. **Implement Base**: `BaseRepository`
3. **Extend**: `UserRepository`

### Template Created

`templates/repository_pattern.ts`

### Recommendation

Adopt this pattern for all data access layers.
```

---

## Related

- `/deep-dive` - Find the source material.
- `/design` - Apply UI patterns.
- `/optimize` - Refactor to use new patterns.
