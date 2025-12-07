---
description: Bootstrap a dedicated worktree and branch for a Linear issue with local config parity
argument-hint: ISSUE_KEY [BASE_BRANCH]
---

Create a worktree for a Linear issue. Uses the @worktree-creator agent (haiku model) for fast, cost-effective execution.

**Arguments**: $ARGUMENTS

## Instructions

1. Parse the arguments:
   - First argument: `ISSUE_KEY` (required) - e.g., `NOD-123`
   - Second argument: `BASE_BRANCH` (optional) - defaults to `origin/main`

2. If no arguments provided, respond with usage:
   ```
   Usage: /cmd:start-linear-issue ISSUE_KEY [BASE_BRANCH]

   Examples:
     /cmd:start-linear-issue NOD-123
     /cmd:start-linear-issue NOD-123 origin/develop
   ```

3. Spawn the @worktree-creator agent with the issue key and optional base branch.

4. After the agent completes, switch to the new worktree directory.
