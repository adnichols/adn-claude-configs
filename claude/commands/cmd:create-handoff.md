---
description: Create handoff document for transferring work to another session
---

# Create Handoff

Create a handoff document to transfer work context to another session. The goal is to compact and summarize your context without losing key details.

## Process

### 1. Gather Metadata

Run these commands to gather context:
```bash
git rev-parse HEAD              # Current commit hash
git branch --show-current       # Current branch
basename $(git rev-parse --show-toplevel)  # Repository name
date -u +"%Y-%m-%dT%H:%M:%SZ"   # ISO timestamp
```

### 2. Determine File Path

Create your file at:
```
thoughts/handoffs/[TICKET]/YYYY-MM-DD_HH-MM-SS_description.md
```

Where:
- `[TICKET]` is the ticket number (e.g., `ENG-123`) or `general` if no ticket
- `YYYY-MM-DD` is today's date
- `HH-MM-SS` is current time in 24-hour format
- `description` is a brief kebab-case description

Examples:
- With ticket: `thoughts/handoffs/ENG-2166/2025-01-08_13-55-22_implement-auth.md`
- Without ticket: `thoughts/handoffs/general/2025-01-08_13-55-22_refactor-api.md`

### 3. Write Handoff Document

Use this template:

```markdown
---
date: [ISO timestamp with timezone]
author: [Your name or "claude"]
git_commit: [Current commit hash]
branch: [Current branch]
repository: [Repository name]
type: handoff
status: complete
tags: [relevant, tags]
last_updated: [YYYY-MM-DD]
---

# Handoff: [Brief Description]

## Task(s)
{Description of tasks with status: completed, in-progress, planned}
{Reference any plan/spec documents you're working from}

## Critical References
{2-3 most important file paths that must be read to continue}
- `thoughts/plans/tasks-fidelity-feature.md` - Implementation plan
- `src/component.ts:45` - Key code location

## Recent Changes
{Code changes made, using file:line syntax}
- `src/feature.ts:120` - Added handler
- `src/test.ts:45` - New test case

## Learnings
{Important discoveries: patterns, root causes, constraints}
- Pattern X works better than Y because...
- Constraint: Must use existing auth flow

## Artifacts
{Exhaustive list of files created or modified}
- `thoughts/plans/tasks-fidelity-feature.md` - Created
- `src/feature.ts` - Modified

## Next Steps
{Action items for the next session}
1. Complete task X
2. Run validation
3. Create PR

## Other Notes
{Additional context that doesn't fit above}
```

## Guidelines

- **More information, not less** - Include everything needed to resume
- **Be thorough and precise** - Include both top-level objectives and details
- **Avoid excessive code snippets** - Use `file:line` references instead
- **Reference all artifacts** - List every document created or modified

## Output

After creating the handoff, respond with:

```
Handoff created! Resume in a new session with:

/cmd:resume-handoff thoughts/handoffs/[path-to-handoff.md]
```
