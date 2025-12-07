---
date: 2025-12-07T21:57:22Z
author: claude
git_commit: 585872a4dd971d2acb9b590569fb79eac186cfd6
branch: main
repository: adn-claude-configs
type: handoff
status: complete
tags: [hl-namespace, worktrees, humanlayer-commands]
last_updated: 2025-12-07
---

# Handoff: HumanLayer Commands Import - Worktree Approach Needs Revision

## Task(s)

**Completed**: Imported 22 HumanLayer commands under `hl` namespace and 6 supporting agents.

The worktree-related commands need a revised approach - the current implementation uses generic placeholders that may not fit your workflow.

## Critical References

- `claude/commands/hl/local_review.md` - Worktree setup for reviewing colleague branches
- `claude/commands/hl/create_worktree.md` - Worktree creation for implementation sessions
- `claude/commands/hl/implement_plan.md` - References worktree paths

## Recent Changes

### Worktree Path Transformations Applied

Changed from hardcoded humanlayer paths to generic placeholders:

- `claude/commands/hl/local_review.md:25` - Changed `git@github.com:USERNAME/humanlayer` to `git@github.com:USERNAME/REPO_NAME`
- `claude/commands/hl/local_review.md:27` - Changed `~/wt/humanlayer/SHORT_NAME` to `~/wt/REPO_NAME/SHORT_NAME`
- `claude/commands/hl/local_review.md:47` - Example now shows `~/wt/REPO_NAME/eng-1696`
- `claude/commands/hl/create_worktree.md:27` - Changed `~/wt/humanlayer/ENG-XXXX` to `~/wt/REPO_NAME/ENG-XXXX`

### Other Key Transformations

- Removed all `humanlayer thoughts sync` commands
- Replaced `mcp__linear__*` with `ltui` CLI commands
- Updated `thoughts/` paths to flat structure (plans/, specs/, research/, etc.)
- Removed hardcoded Linear team/project/label IDs from `linear.md`

## Learnings

- The original HumanLayer commands had tight coupling to:
  1. `humanlayer thoughts sync` CLI for syncing thoughts directories
  2. Specific worktree paths at `~/wt/humanlayer/`
  3. A `hack/create_worktree.sh` script
  4. Linear MCP tools with hardcoded IDs

- Worktree commands assume a specific workflow pattern where thoughts/ is synced between main repo and worktrees

## Artifacts

### New Agents (claude/agents/)
- `codebase-locator.md`
- `codebase-analyzer.md`
- `codebase-pattern-finder.md`
- `thoughts-locator.md` (updated with flat directory structure)
- `thoughts-analyzer.md`
- `web-search-researcher.md`

### New Commands (claude/commands/hl/)
All 22 commands listed in the plan at `/Users/anichols/.claude/plans/bright-riding-porcupine.md`

## Next Steps

1. **Revise worktree approach** - Determine how worktrees should work in your setup:
   - What base path for worktrees? (currently `~/wt/REPO_NAME/`)
   - How should thoughts/ be shared/synced between worktrees?
   - Do you have a worktree creation script to reference?

2. **Review linear.md** - May need project-specific configuration

3. **Test commands** - Run a few hl/ commands to verify they work as expected

## Other Notes

The plan file at `/Users/anichols/.claude/plans/bright-riding-porcupine.md` contains the full transformation details.

Commands excluded from import (personal shortcuts):
- `ralph_impl.md`, `ralph_plan.md`, `ralph_research.md`
- `oneshot.md`, `oneshot_plan.md`
