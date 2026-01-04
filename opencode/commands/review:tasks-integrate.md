---
description: Integrate task review comments by fixing inaccuracies
argument-hint: "<path to task list>"
---

# Integrate Task List Review Comments

Fix all inaccuracies identified by reviewers in the task list, ensuring tasks accurately reflect the source specification.

**Task list to integrate:** $ARGUMENTS

## Process

### 1. Read and Catalog All Comments

Read the task list and extract all HTML comments from reviewers. Catalog each comment by:
- **Reviewer**: Claude, Gemini, Codex, GPT, or other identifiers
- **Type**: INCORRECT, SCOPE DRIFT, MISINTERPRETATION, CONTRADICTION, WRONG REFERENCE
- **Task**: Which task/subtask it references
- **Response comments**: Any `RE:` responses from other reviewers

Create a working list of all inaccuracies to fix.

### 2. Read the Source Specification

Extract the **Source Specification** path from the task list header (in the "Implementation Authority" section).

Read the source specification completely to understand:
- Exact requirements as written
- Technical decisions and constraints
- Scope boundaries (included/excluded)
- Success criteria

### 3. Verify Each Comment Against Spec

For each reviewer comment:
1. Locate the referenced section in the source specification
2. Confirm whether the comment is valid (task differs from spec)
3. Determine the correct content based on the spec

If reviewers disagree, the **specification is the authority** - use it to determine which reviewer is correct.

### 4. Fix Each Inaccuracy

For each confirmed inaccuracy, apply the appropriate fix:

**INCORRECT** - Rewrite task to match what spec actually says
```markdown
Before: "- [ ] 2.3 Add JWT validation to auth middleware"
After:  "- [ ] 2.3 Add session-based validation to auth middleware"
```

**SCOPE DRIFT** - Remove the out-of-scope content or reduce scope
```markdown
Before: "- [ ] 4.2 Build admin dashboard with user management"
After:  (deleted - admin dashboard excluded from spec)
```

**MISINTERPRETATION** - Rewrite to match spec intent
```markdown
Before: "- [ ] 3.1 Cache responses indefinitely with manual invalidation"
After:  "- [ ] 3.1 Cache responses for 5 minutes with automatic expiry"
```

**WRONG REFERENCE** - Correct file paths, APIs, or component names
```markdown
Before: "- [ ] 1.2 Update src/services/userService.ts"
After:  "- [ ] 1.2 Update src/services/user.service.ts"
```

**CONTRADICTION** - Resolve to match specification
```markdown
Before: "- [ ] 5.1 Return 404 for missing resources"
After:  "- [ ] 5.1 Return 204 for missing resources (per spec section 4.2)"
```

### 5. Remove Resolved Comments

After fixing each inaccuracy, remove the corresponding HTML comment from the task list.

### 6. Handle Disputes

If multiple reviewers commented on the same task with different opinions:
1. Check the specification - it is the final authority
2. Apply the fix that matches the specification
3. If specification is ambiguous on this point, use AskUserQuestion to clarify

### 7. Summary Report

After all fixes are applied, provide a summary:

```markdown
## Integration Complete

**Task list:** [path]
**Source spec:** [path]

### Corrections Made
| Task | Type | Before | After |
|------|------|--------|-------|
| 2.3 | INCORRECT | JWT validation | Session-based validation |
| 4.2 | SCOPE DRIFT | (removed) | Admin dashboard excluded |
| ... | ... | ... | ... |

### Summary
- Total comments processed: N
- Corrections made: N
- Tasks removed (scope drift): N
- Comments where reviewers agreed: N
- Disputes resolved via spec: N

### Verification
- [ ] All reviewer comments removed
- [ ] All tasks now match specification
- [ ] Task list ready for implementation
```

## Decision-Making Guidelines

**Always defer to the specification:**
- If a reviewer's comment conflicts with the spec, the spec wins
- If the spec is ambiguous, ask the user rather than guessing
- Never add requirements beyond what the spec states

**When to ask the user:**
- Specification genuinely doesn't cover the point in question
- Multiple valid interpretations of the specification exist
- Fixing would significantly change the implementation approach

## Output

The task list file should be updated in place with:
- All inaccuracies corrected to match specification
- All reviewer comments removed
- Clean task list ready for `/dev:3:process-tasks`

---

## ➡️ Next Steps

After integration completes, the task list is ready for:
```
/dev:3:process-tasks <path to task list>
```
