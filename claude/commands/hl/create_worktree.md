---
description: Create worktree and launch implementation session for a plan
---

## Setup Worktree for Implementation

**Ticket Prefix**: Derive from `.ltui.json` team field if present (e.g., `"team": "NOD"` → use `NOD-`).
Otherwise extract from issue key argument.

1. Compute repo paths:
   ```bash
   REPO_ROOT=$(git rev-parse --show-toplevel)
   REPO_NAME=$(basename "$REPO_ROOT")
   REPO_PARENT=$(dirname "$REPO_ROOT")
   TICKET_LOWER=$(echo "$TICKET" | tr '[:upper:]' '[:lower:]')
   WORKTREE_PATH="$REPO_PARENT/${REPO_NAME}-${TICKET_LOWER}"
   ```

2. Create worktree with the Linear branch name:
   ```bash
   git worktree add -b "$TICKET_LOWER" "$WORKTREE_PATH" origin/main
   ```

3. Determine required data:
   - Branch name
   - Path to plan file (use relative path only)
   - Launch prompt
   - Command to run

**IMPORTANT PATH USAGE:**
- The thoughts/ directory is synced between the main repo and worktrees
- Always use ONLY the relative path starting with `thoughts/...` without any directory prefix
- Example: `thoughts/plans/fix-mcp-keepalive-proper.md` (not the full absolute path)
- This works because thoughts are synced and accessible from the worktree

4. Confirm with the user by sending a message:

```
Based on the input, I plan to create a worktree with the following details:

worktree path: $REPO_PARENT/${REPO_NAME}-${TICKET_LOWER}
branch name: BRANCH_NAME
path to plan file: $FILEPATH
launch prompt:

    /implement_plan at $FILEPATH and when you are done implementing and all tests pass, read ./claude/commands/commit.md and create a commit, then read ./claude/commands/describe_pr.md and create a PR, then add a comment to the Linear ticket with the PR link

command to run:

```

Incorporate any user feedback then proceed.
