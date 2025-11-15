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
- Use the `linear` CLI to pull full issue metadata for the supplied key. Confirm it belongs to the "Doc Thingy" project; stop with a warning if not.

## Linear CLI Commands Reference

The `linear` CLI tool provides the following commands needed for this workflow:

### Fetching Issue Details
```bash
# Get single issue with full details (human-readable output)
linear issue <ISSUE_ID>

# Get issue in JSON format (use filter query for structured data)
linear issues --filter "id:<ISSUE_ID>" --format json --limit 1

# Example JSON output structure:
# [
#   {
#     "id": "abc123",
#     "identifier": "ENG-123",
#     "title": "Issue title",
#     "description": "Issue description",
#     "state": {"name": "In Progress", "type": "started"},
#     "priority": 2,
#     "assignee": {"name": "John Doe", "email": "john@example.com"},
#     "project": {"name": "Project Name", "id": "proj123"},
#     "labels": [{"name": "bug"}],
#     "url": "https://linear.app/team/issue/ENG-123"
#   }
# ]
```

### Listing Projects
```bash
# List all projects (human-readable)
linear projects

# To get project details in JSON, use issues filter:
linear issues --filter "project:<PROJECT_NAME>" --format json --limit 1
```

### Listing and Filtering Issues
```bash
# List issues with various filters (supports --format json)
linear issues --format json --limit 50

# Filter by team
linear issues --team ENG --format json

# Filter by project
linear issues --filter "project:Doc Thingy" --format json

# Filter by assignee
linear issues --assignee user@example.com --format json

# Search by title
linear issues --search "bug" --format json

# Advanced filtering examples:
linear issues --filter "assignee:john@example.com AND priority:>2" --format json
linear issues --filter "has-label:urgent AND state:started" --format json
```

### Verifying Authentication
```bash
# Check if authenticated and get current user info
linear whoami

# If not authenticated, guide user to run:
linear auth
```

### Parsing Issue Data
When fetching issue metadata:
1. Use `linear issues --filter "id:<ISSUE_KEY>" --format json --limit 1` to get structured JSON
2. Parse the JSON to extract: `title`, `description`, `project.name`, `state.name`, `labels`, `url`
3. Verify `project.name` equals "Doc Thingy" (case-sensitive)
4. If the project doesn't match, halt with: "Error: Issue <ISSUE_KEY> belongs to project '<actual-project>', not 'Doc Thingy'"

### Error Handling
- If `linear issues --filter "id:<ISSUE_KEY>"` returns empty array `[]`, the issue doesn't exist
- If `linear whoami` fails, the user needs to authenticate with `linear auth`
- All commands may fail if not authenticated - check auth status first

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

### Environment & Config Files
- Identify environment/config files in the root repository that exist but are git-ignored, including:
  - All `.env*` variants (e.g., `.env`, `.env.local`, `.env.development`, `.env.test.local`)
  - `.envrc`
  - `*.local` or `*.local.*` under `config/`, `settings/`, or `scripts/`
  - `*.private.*`, `docker-compose.override.yml`, `package-lock.private.json`
- Use `find` combined with `git check-ignore -vq` to detect which files are present locally yet ignored.
- Copy each discovered file or directory into the worktree using `rsync -avh --relative` so directory structures are preserved.
- Mirror executable bits (`chmod --reference`) and re-run `direnv allow` if an `.envrc` was copied.
- Log every copied path; warn (do not fail) when expected files listed in `SETUP.md`, `README.md`, or `.env.example` are absent.

### MCP Server Configuration (Non-Linear)
Copy MCP server configuration from the main repository to the worktree (for non-Linear MCP servers):

1. **Copy MCP Configuration**:
   - Create `.claude/` directory in the worktree if it doesn't exist
   - Copy `.claude/mcp-servers.json` from the repository root to the worktree if it exists
   - This ensures other MCP servers (e.g., Playwright, GitHub) remain available in the worktree

2. **Linear CLI Authentication**:
   - The `linear` CLI uses its own authentication (typically via `linear auth`)
   - Verify the CLI is authenticated by running `linear whoami` - if it fails, guide user to run `linear auth`
   - No environment variables need to be propagated for Linear CLI (authentication is global per user)

3. **Other MCP Server Environment Variables**:
   - Scan `.claude/mcp-servers.json` for non-Linear MCP servers with `env` fields
   - Copy any required environment variables to the worktree's `.env.local` or `.envrc`
   - Common variables: `GITHUB_TOKEN`, `SLACK_TOKEN`, etc. (NOT `LINEAR_API_KEY` since we use CLI)

## Linear Context Notes
- Create (or update) `notes/linear/<issue-key-lower>.md` inside the worktree (create directories as needed) summarizing the Linear issue: title, description, acceptance criteria, labels, and link.
- Record the branch name, worktree path, base ref, and timestamp in the note for future handoff.

## Finalize Session
- Switch Claude Code working directory to the new worktree so subsequent commands run there.
- Print a ready-state checklist:
  - Worktree location & branch
  - Linear issue summary (title, URL, project)
  - Config files copied
  - Linear CLI authentication status (from `linear whoami`)
  - MCP servers configured (non-Linear servers)
  - Next suggested commands (install deps, run tests, etc.) derived from repository docs
- Leave the original repository untouched aside from the new worktree metadata and branch creation.
