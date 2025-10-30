---
description: Fully execute a Linear issue autonomously from worktree setup through PR submission
argument-hint: ISSUE_KEY [BASE_BRANCH]
---

Stand up a dedicated worktree for the given Linear issue and carry the fix to completion without additional operator prompts. Accept the Linear issue key as the first argument (for example `NOD-123`). Optionally accept a second argument that overrides the default base branch (`origin/main`). Think harder.

## Inputs & Preconditions
- Require at least one argument; fail fast with guidance if missing.
- Verify the repository root (`git rev-parse --show-toplevel`) has no staged or unstaged changes; halt if dirty until the operator cleans up.
- `git fetch --prune --tags` before branching to avoid stale bases.
- Retrieve full Linear issue metadata via MCP (title, description, project, status, labels, attachments) and confirm it belongs to the "Doc Thingy" project. Abort with a warning if not.
- Record the Linear issue URL for later status updates and PR descriptions.

## Branch & Worktree Creation
1. Generate a slug from the Linear issue title: lowercase, alphanumerics only, spaces → hyphens, collapse repeats, cap at 6 words / 48 characters.
2. Branch name: `issue/<issue-key-lower>/<slug>`.
3. Compute repo root and parent; define worktree path `<repo-parent>/<repo-name>-<issue-key-lower>-<slug>`. Never nest under an existing Git repository.
   - If the path already exists as a worktree for this branch, prune/reset via `git worktree remove --force` or fast-forward.
   - If the path exists but is unrelated, halt and ask the operator how to proceed.
   - Validate the target path is outside any Git repo (`git -C <path> rev-parse` should fail).
4. Create the worktree: `git worktree add --track -b <branch> <worktree-path> <base-ref>` where `<base-ref>` defaults to `origin/main` or the supplied override.
5. Inside the new worktree, set upstream tracking and confirm `git status` is clean.

## Propagate Local Configuration
- Discover ignored-but-present assets to mirror into the worktree:
  - All `.env*` variants (e.g., `.env`, `.env.local`, `.env.test.local`, `.env.development`)
  - `.envrc`
  - `*.local` or `*.local.*` under `config/`, `settings/`, `scripts/`
  - `*.private.*`, `docker-compose.override.yml`, `package-lock.private.json`
- Use `find` plus `git check-ignore -vq` to detect candidates; copy with `rsync -avh --relative` and preserve permissions (`chmod --reference`).
- Re-run `direnv allow` when `.envrc` is copied. Log every copied path; warn (not fail) if expected env files mentioned in docs are missing.

## Linear Context Capture
- Create `notes/linear/<issue-key-lower>.md` in the worktree summarizing issue metadata, acceptance criteria, branch, worktree path, base ref, and timestamp.
- Track open questions and assumptions in the note as work progresses.

## Autonomous Execution Flow
1. **Orientation**
   - Parse the Linear description, attachments, and comments into explicit requirements, acceptance criteria, non-goals, and test expectations.
   - Identify referenced files, components, or endpoints via `rg`, repository docs, or previous commits.
   - Draft a short execution plan (tasks, validations) in the worktree note; keep it updated.
2. **Implementation Loop**
   - Execute tasks sequentially using repo standards (consult `CLAUDE.md`, `TESTING.md`, `AGENTS.md`).
   - Implement code changes directly in the worktree. Use `@developer` or `@developer-fidelity` agents as helpers when needed; do not pause for human approval unless blocked.
   - Maintain incremental commits logically grouped or a single commit at the end per repo conventions.
3. **Validation**
   - Run required checks (tests, linters, builds). Prioritize commands specified in repo docs or the Linear issue.
   - If a check fails, remediate and rerun until clean or until three attempts fail; on repeated failure escalate to operator with diagnostics while leaving the workspace intact.
4. **Documentation & Status Updates**
   - Update the worktree note with implementation summary, commands run, and remaining risks.
   - Post a draft update to Linear via MCP (comment) summarizing progress when major milestones complete or a blocker arises.

## Completion & Hand-off
- Stage and commit changes using a conventional commit message referencing the Linear key (e.g., `git commit -m "fix: resolve <short description>" -m "Refs <ISSUE_KEY>"`).
- Push the branch (`git push -u origin <branch>`). Handle force-push only if branch already exists and operator consent is implicit.
- Auto-create a pull request (GitHub CLI or equivalent) with:
  - Title `[<ISSUE_KEY>] <Linear title>`
  - Body including summary, validation commands, checklist of acceptance criteria, and Linear issue URL.
- Transition the Linear issue state to "In Review" (or appropriate) and add a comment linking the PR.
- Present a final Codex summary: branch, PR URL, test results, remaining concerns. If work is incomplete, clearly outline blockers and leave the issue in the appropriate Linear state without creating a PR.
- Keep the primary repo pristine aside from worktree metadata and pushed branch.
