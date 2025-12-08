---
description: Implement plans tracked in beads issues
---

# Implement Plan (Beads-Only)

You are tasked with implementing work tracked in beads. The beads issues contain all implementation details including code snippets, file paths, and success criteria.

**Beads is the sole source of truth. There are no separate plan files.**

## Getting Started

1. **Check for existing work**:
   ```bash
   bd list --status=in_progress   # Resume active work
   bd ready                       # Find available work if nothing in progress
   ```

2. **If given a specific issue ID**, show its details:
   ```bash
   bd show <id>
   ```

3. **Read files mentioned in the issue** - read them FULLY (no limit/offset)

4. **If no work is in progress and none specified**, ask:
   ```
   No implementation work is currently in progress.

   Run `bd ready` to see available issues, or provide a specific issue ID to work on.
   ```

## Implementation Philosophy

Beads issues are carefully designed, but reality can be messy. Your job is to:
- Follow the issue's intent while adapting to what you find
- Complete each issue fully before moving to the next
- Verify your work makes sense in the broader codebase context

When things don't match the issue exactly, think about why and communicate clearly.

If you encounter a mismatch:
- STOP and think deeply about why the issue can't be followed as written
- Present the problem clearly:
  ```
  Issue with <id>:
  Expected: [what the issue describes]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

## Workflow

### Starting Work
```bash
bd show <id>                           # Review issue details
bd update <id> --status in_progress    # Claim the work
```

### During Implementation
- Read all files mentioned in the issue FULLY
- Implement the changes described
- Run verification commands listed in the issue
- Fix any issues before marking complete

### Completing Work
```bash
bd close <id> --reason "Completed"     # Mark done
bd show <next-id>                      # Review next issue
bd update <next-id> --status in_progress
```

### Discovered Work
If you find additional tasks needed:
```bash
bd create --title "Found: [description]" --type task
bd dep add <new-id> <current-id>       # New task blocks current if needed
```

### Blocked
If you hit a blocker:
```bash
bd create --title "Blocker: [description]" --type bug -p 1
bd dep add <current-id> <blocker-id>   # Current depends on blocker
```

## Verification

After implementing an issue:

1. **Run automated checks** listed in the issue (usually `pnpm test:unit && pnpm build`)
2. **Fix any failures** before proceeding
3. **Pause for manual verification** if the issue includes manual steps:
   ```
   Issue <id> Complete - Ready for Manual Verification

   Automated verification passed:
   - [List automated checks that passed]

   Please perform the manual verification steps from the issue:
   - [List manual verification items]

   Let me know when manual testing is complete so I can proceed.
   ```

If instructed to execute multiple issues consecutively, skip the pause until the last one.

## Resuming Work

When resuming a session:
```bash
bd list --status=in_progress    # Find where you left off
bd show <id>                    # Review the issue details
```

- Trust that closed issues are complete
- Pick up from the in_progress issue
- Verify previous work only if something seems off

## Session End

Always sync before ending:
```bash
bd sync
```

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.
