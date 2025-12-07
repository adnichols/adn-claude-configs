---
description: Resume work from a handoff document
argument-hint: [path or TICKET]
---

# Resume from Handoff

Resume work from a handoff document created by `/cmd:create-handoff`. The argument can be:
- A full path: `thoughts/handoffs/ENG-123/2025-01-08_13-55-22_description.md`
- A ticket number: `ENG-123` (will find the most recent handoff for that ticket)

Handoff path or ticket: $ARGUMENTS

## Process

### 1. Locate Handoff Document

If a ticket number is provided:
1. Search `thoughts/handoffs/[TICKET]/` for the most recent handoff
2. Sort by filename timestamp (most recent first)
3. Use the most recent one

If a path is provided:
1. Read the file directly

### 2. Read and Parse Handoff

Read the handoff document completely. Extract:
- Task status and descriptions
- Critical references to read
- Recent changes made
- Learnings and constraints discovered
- Artifacts created
- Next steps

### 3. Read Critical References

Read ALL files listed in "Critical References" section directly (not with sub-agents).
These are essential for understanding the current state.

### 4. Verify Current State

**IMPORTANT: Never assume handoff state matches current state.**

Launch focused research tasks to verify:
1. Check if referenced files still exist at stated locations
2. Verify code changes mentioned are still present
3. Check git status for any new changes since handoff
4. Confirm branch is correct

```bash
git status
git log --oneline -5
git diff --stat HEAD~3
```

### 5. Present Analysis

Present a comprehensive analysis to the user:

```markdown
## Handoff Resume Analysis

### Original Tasks
{List tasks and their status from handoff}

### Verification Status
- [ ] Critical files verified
- [ ] Recent changes confirmed
- [ ] Branch status: [branch name]
- [ ] New changes since handoff: [yes/no]

### Learnings from Previous Session
{Key learnings that apply to continued work}

### Recommended Action Plan
1. {First action based on handoff next steps}
2. {Second action}
3. ...

### Questions/Clarifications Needed
{Any ambiguities or questions before proceeding}
```

### 6. Get Confirmation

Ask the user to confirm the action plan before proceeding.

### 7. Begin Work

Once confirmed, begin working through the action plan. Reference learnings from the handoff throughout.

## Guidelines

- **Verify, don't assume** - Always check current state against handoff claims
- **Read references directly** - Don't delegate critical file reading to sub-agents
- **Present before acting** - Get user confirmation before making changes
- **Apply learnings** - Use discovered patterns and constraints from handoff

## Example

```
/cmd:resume-handoff ENG-2166
```

Will find the most recent handoff in `thoughts/handoffs/ENG-2166/` and resume from there.
