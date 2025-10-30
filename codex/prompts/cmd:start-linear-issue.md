---
description: Bootstrap a dedicated worktree and branch for a Linear issue with local config parity
argument-hint: ISSUE_KEY [BASE_BRANCH]
---

Spin up a ready-to-code environment for a Linear issue. Accept the Linear issue key as the first argument (for example `NOD-123`). Optionally accept a second argument that overrides the default base branch (`origin/main`). Think harder. 

Linear issue and optional base branch: $ARGUMENTS 

## Inputs & Preconditions
- Require at least one argument; fail fast with guidance if missing.
- Verify the working tree at repo root is clean (`git status --porcelain=v1`); halt and request operator cleanup if dirty.
- Run `git fetch --prune --tags` before branching so worktrees never start from stale refs.
- Use the Linear MCP client to pull full issue metadata (title, description, project, status) for the supplied key. Confirm it belongs to the "Doc Thingy" project; stop with a warning if not.

## Branch & Worktree Creation
1. The branch and worktree should simply be the Linear issue (e.g., nod-123).
2. Compose branch name: `<issue-key-lower>`.
3. Compute the repo root (`git rev-parse --show-toplevel`) and its parent directory. Construct an absolute worktree path outside the repository: `<repo-parent>/<repo-name>-<issue-key-lower>`. Never place worktrees inside the repo.
   - If a directory already exists at that path and is a worktree for the same branch, prune/reset it to the latest base via `git worktree remove --force` then recreate, or fast-forward within that directory.
   - If it exists but points elsewhere, halt and ask the operator how to proceed.
   - Validate the chosen path is not nested under any Git working tree by checking `git -C <path> rev-parse` (expect failure).
4. Create the worktree using `git worktree add --track -b <branch> <worktree-path> <base-ref>` where `<base-ref>` defaults to `origin/main` or the supplied second argument.
5. Inside the new worktree, configure tracking (`git branch --set-upstream-to=<base-remote>`) and confirm `git status` is clean.

## Propagate Local Configuration
Ensure the worktree mirrors indispensable local assets that are not committed:
- Identify environment/config files in the root repository that exist but are git-ignored, including:
  - All `.env*` variants (e.g., `.env`, `.env.local`, `.env.development`, `.env.test.local`)
  - `.envrc`
  - `*.local` or `*.local.*` under `config/`, `settings/`, or `scripts/`
  - `*.private.*`, `docker-compose.override.yml`, `package-lock.private.json`
- Use `find` combined with `git check-ignore -vq` to detect which files are present locally yet ignored.
- Copy each discovered file or directory into the worktree using `rsync -avh --relative` so directory structures are preserved.
- Mirror executable bits (`chmod --reference`) and re-run `direnv allow` if an `.envrc` was copied.
- Log every copied path; warn (do not fail) when expected files listed in `SETUP.md`, `README.md`, or `.env.example` are absent.

## Linear Context Notes
- Create (or update) `notes/linear/<issue-key-lower>.md` inside the worktree (create directories as needed) summarizing the Linear issue: title, description, acceptance criteria, labels, and link.
- Record the branch name, worktree path, base ref, and timestamp in the note for future handoff.

## Finalize Session
- Switch Codex working directory to the new worktree so subsequent commands run there.
- Print a ready-state checklist:
  - Worktree location & branch
  - Config files copied
  - Next suggested commands (install deps, run tests, etc.) derived from repository docs
- Leave the original repository untouched aside from the new worktree metadata and branch creation.
