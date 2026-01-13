---
description: Integrate task review comments by fixing inaccuracies
argument-hint: "<path to task list>"
---

# Integrate Task List Review Comments

Fix all inaccuracies identified by reviewers in the task list, ensuring tasks accurately reflect the source specification.

**Task list to integrate:** $ARGUMENTS

## Process

### 0. Gather Comment Files

Locate and read all comment files from reviewers.

**Option 1 - Review file pattern** (if review files are in the same directory as tasks):
- `{task_path}.review-qwen.md`
- `{task_path}.review-kimi.md`
- `{task_path}.review-deepseek.md`

**Option 2 - Filename-based pattern** (extract filename without path/extension):
- Extract the filename (without path and extension) from `task_path`
- `{task_filename}.review-qwen.md`
- `{task_filename}.review-kimi.md`
- `{task_filename}.review-deepseek.md`

Check both patterns and read any files that exist. If a reviewer failed or produced no comments, that comment file may be missing - this is acceptable.

Read all available comment files. If none exist, inform the user that no review data was found and abort.

### 1. Read and Catalog All Comments

From the comment files, extract all reviewer feedback and parse each comment to extract:
- **Reviewer**: Qwen, Kimi, or DeepSeek
- **Line Number**: Which line of the task list it references
- **Category**: INCORRECT, SCOPE DRIFT, MISINTERPRETATION, CONTRADICTION, or WRONG REFERENCE
- **Content**: The actual comment feedback

Create a working list of all inaccuracies to fix.

### 2. Read the Task List and Source Specification

Read the task list file to:
- Understand the full context
- Locate the lines referenced in comments
- Have the proper content to update

Extract the **Source Specification** path from the task list header.
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

For each confirmed inaccuracy, apply the appropriate fix at the specified line number:

**INCORRECT** - Rewrite task to match what spec actually says
```markdown
Before: "- [ ] 2.3 Add JWT validation to auth middleware"
After:  "- [ ] 2.3 Add session-based validation to auth middleware"
```

**SCOPE DRIFT** - Remove the out-of-scope content or reduce scope
```markdown
Before: "- [ ] 4.2 Build admin dashboard with user management"
After:  (delete entire line - admin dashboard excluded from spec)
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

For each fix:
1. Find the line number specified in the comment
2. Apply the appropriate edit using the exact oldString/newString
3. Verify the fix aligns with the source specification

### 5. Handle Disputes

If multiple reviewers commented on the same task or area with different opinions:
1. Check the specification - it is the final authority
2. Apply the fix that matches the specification
3. If specification is ambiguous on this point, use AskUserQuestion to clarify

### 6. Clean Up Temporary Files

After successful integration, delete the comment files:

```bash
rm -f {task_path}.review-qwen.md
rm -f {task_path}.review-kimi.md
rm -f {task_path}.review-deepseek.md
```

The reviews are preserved in git history if committed, and the summary report documents all corrections.

If integration fails (e.g., due to an error mid-process), KEEP the comment files so the user can debug or manually reconcile.

### 7. Summary Report

After all fixes are applied, provide a summary:

```markdown
## Integration Complete

**Task list:** {task-path}
**Source spec:** {spec-path}

### Corrections Made
| Type | Count |
|------|-------|
| INCORRECT | {N} |
| SCOPE DRIFT | {N} |
| MISINTERPRETATION | {N} |
| CONTRADICTION | {N} |
| WRONG REFERENCE | {N} |

### Summary
- Total comments processed: {N}
- Corrections made: {N}
- Tasks removed (scope drift): {N}
- Comments per reviewer:
  - Qwen: {N}
  - Kimi: {N}
  - DeepSeek: {N}
- Comments where reviewers agreed: {N}
- Disputes resolved via spec: {N}

### Verification
- [ ] All reviewer comments integrated
- [ ] All tasks now match specification
- [ ] Comment files deleted
- Task list ready for /dev:3:process-tasks
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
- All reviewer comments integrated
- Clean task list ready for `/dev:3:process-tasks`

The temporary comment files should be deleted after successful integration. If integration fails, comment files are preserved for debugging.

---

## ➡️ Next Steps

After integration completes, the task list is ready for:
```
/dev:3:process-tasks <path to task list>
```
