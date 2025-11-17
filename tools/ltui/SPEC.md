# ltui — Linear Agent CLI Specification

Token‑efficient CLI for AI coding agents to interact with Linear while working on bugs and features.

This document defines goals, constraints, command surface, output contracts, and implementation details for the initial `ltui` repository.

---

## 1. Goals and Non‑Goals

**Goals**
- Provide a high‑density, token‑efficient interface for AI coding agents to interact with Linear issues.
- Cover the majority of commonly used Linear API operations via the official SDK (`@linear/sdk`).
- Work across local projects: API keys and configuration are stored in a global, user‑level location, not per‑repo.
- Be safely scriptable and deterministic: same command + same Linear state → same output bytes.
- Support structured CLI usage in “agent mode” with minimal/no ANSI escape sequences.
- Make it trivial for agents to:
  - Find relevant issues (search/filter).
  - Inspect issue details and history.
  - Add comments and links to PRs/branches.
  - Update issue states, assignments, labels, and estimates.
  - Create new issues inside specific Linear projects, with specific labels and initial states.
  - Change the state of issues as part of automated workflows.
  - Configure per-project alignment between local codebases and Linear projects/teams.

**Non‑Goals (initially)**
- Full coverage of every Linear object and mutation (but design must be extensible).
- Acting as a generic GraphQL client (it is opinionated around Linear models).
- Managing git branches or VCS directly (can expose fields for tools that do).
- Providing a rich, mouse‑driven UI; keyboard + CLI focus only.

---

## 2. High‑Level Design

`ltui` is a Node.js/TypeScript CLI application with a structured command API designed for AI agents. There is **no** curses or full‑screen TUI layer; all interaction is via line‑oriented CLI commands and stdout.

- **Core layer (CLI API):**
  - Subcommands for core entities: `auth`, `issues`, `teams`, `projects`, `cycles`, `labels`, `users`.
  - Deterministic text output optimized for LLM consumption.
  - No interactive prompts by default (explicit flags for anything that might prompt).

- **Agent mode (default / when `LTUI_AGENT_MODE=1`):**
  - No colors or fancy box‑drawing.
  - Compact, predictable line‑oriented formats.
  - Optional `--format` and `--fields` controls to tune density.

All usage is expected to be through the **CLI surface in agent mode**; there is no interactive TUI.

---

## 3. Technology Choices

- **Language:** TypeScript (strict mode).
- **Runtime:** Node.js ≥ 20.
- **Linear API:** [`@linear/sdk`](https://github.com/linear/linear) (generated, typed client).
- **CLI framework:** `commander` or `yargs` (simple, stable).
- **UI constraints:** no curses/full‑screen UI; output is plain, line‑oriented text only.
- **Config/Storage:**
  - Default config directory: `~/.config/ltui/` (overridable with `LTUI_CONFIG_DIR`).
  - Files:
    - `config.json` – global configuration and profile metadata.
    - `profiles.json` – per‑profile Linear API keys (optionally stored via OS keychain).
  - Optional per‑project overrides via `.ltui.json` in the current repo.

Per‑project configuration enables aligning a local codebase with a specific Linear team/project, so agents can omit repetitive flags when creating or updating issues.

---

## 4. Authentication and Configuration

### 4.1 Profiles

`ltui` supports multiple **profiles**, each mapping to a Linear workspace/account.

Example `~/.config/ltui/config.json`:

```json
{
  "defaultProfile": "personal",
  "profiles": {
    "personal": {
      "workspace": "my-workspace",
      "keyRef": "personal"
    },
    "work": {
      "workspace": "company-workspace",
      "keyRef": "work"
    }
  }
}
```

API keys are stored separately (see below) and referenced by `keyRef`.

### 4.2 API Key Storage

Design goals:
- Available across all local projects.
- Easy to set up from the shell.
- Secure by default, but practical for local agent use.

Implementation:
- Keys are stored either:
  - In the OS keychain (preferred, when available).
  - Or in `~/.config/ltui/profiles.json` with file mode `0600`.
- Environment overrides:
  - `LINEAR_API_KEY` – highest precedence for the current process.
  - `LTUI_PROFILE` – default profile to use when not explicitly specified.

Example `profiles.json` (file‑based storage):

```json
{
  "personal": {
    "apiKey": "lin_api_xxx"
  },
  "work": {
    "apiKey": "lin_api_yyy"
  }
}
```

### 4.3 Per‑Project Alignment

Per‑project alignment is configured via a `.ltui.json` file at the root of a local repo (or any directory). This file allows agents to implicitly target the correct Linear team/project, apply default labels, and set default states when creating new issues.

Example `.ltui.json`:

```json
{
  "profile": "work",
  "teamKey": "ENG",
  "projectId": "12345678-aaaa-bbbb-cccc-1234567890ab",
  "defaultIssueState": "Todo",
  "defaultLabels": ["bug", "backend"],
  "defaultAssignee": "me"
}
```

Semantics:
- `profile` – optional; overrides `LTUI_PROFILE` / global default when running under this directory.
- `teamKey` – default team key used when `--team` is omitted.
- `projectId` – default Linear project for new issues when `--project` is omitted.
- `defaultIssueState` – default state for newly created issues when `--state` is omitted.
- `defaultLabels` – labels automatically applied to new issues (unless overridden by flags).
- `defaultAssignee` – default assignee for new issues (e.g. `"me"` or a user id).

Commands must consult `.ltui.json` for defaults, but explicit CLI flags always take precedence.

### 4.4 Auth Commands

- `ltui auth list`
  - Lists configured profiles and whether they have a usable key.
- `ltui auth add --profile <name> [--workspace <slug>] [--api-key <key>]`
  - Adds/updates a profile; `--api-key` can be omitted to read from `LINEAR_API_KEY`.
- `ltui auth remove --profile <name>`
- `ltui auth test [--profile <name>]`
  - Validates connectivity and prints basic account information in compact form.

---

## 5. Command Surface

The CLI is organized by top‑level noun commands. Every command:
- Has a stable, documented output format.
- Supports `--profile`, `--format`, `--fields`, and `--limit` (when relevant).
- Exits non‑zero on failure with a compact `ERROR:` header line.

### 5.1 Global Flags

- `--profile <name>` – use a specific profile.
- `--format <fmt>` – output format:
  - `tsv` (default; most token‑efficient),
  - `table` (more readable, for troubleshooting),
  - `detail` (key/value pairs),
  - `json` (compact JSON, no whitespace).
- `--fields <comma-separated>` – limit fields included in output.
- `--limit <n>` – limit item count for list operations (default 20).
- `--cursor <cursor>` – pagination cursor for list operations.
- `--agent` / `--no-agent` – force agent mode on/off.

### 5.2 Issues

`ltui issues` is the core surface for bug‑fix workflows.

#### 5.2.1 List Issues

- `ltui issues list [filters...]`
  - Filters (all optional, combinable):
    - `--team <key-or-id>`
    - `--project <key-or-id>`
    - `--state <name-or-id>` (e.g. `"Todo"`, `"In Progress"`, `"Done"`)
    - `--assignee <me|email|id>`
    - `--label <name-or-id>` (repeatable)
    - `--search <query>` (Linear search syntax, if available)
    - `--updated-since <iso>` / `--created-since <iso>`
  - Default sort: updated desc.

**Agent TSV format (default in agent mode):**

Header row followed by one line per issue:

```text
id	key	identifier	title	state	priority	assignee	labels	project	updatedAt
<id>	<key>	<identifier>	<title>	<state>	<priority>	<assignee>	<labels>	<project>	<iso>
```

- `identifier` is the human key like `ENG-123`.
- `labels` is a `,`‑joined list of label names.
- `assignee` and `project` use compact human names or `-` if empty.

#### 5.2.2 View Issue

- `ltui issues view <issue-id-or-key> [--include-comments] [--include-history]`

**Agent detail format (default in agent mode):**

```text
ISSUE: <identifier> (<id>)
TITLE: <title>
STATE: <state>
PRIORITY: <priority-or-none>
TEAM: <team-key-or-name>
PROJECT: <project-or-none>
ASSIGNEE: <assignee-or-none>
LABELS: <comma-separated-labels-or-none>
CREATED_AT: <iso>
UPDATED_AT: <iso>
DESCRIPTION_START
<markdown description, possibly truncated>
DESCRIPTION_END
```

When `--include-comments`:

```text
COMMENTS_START
<comment-id>	<author>	<iso>	<body-one-line-or-truncated>
...
COMMENTS_END
```

When `--include-history`:

```text
HISTORY_START
<iso>	<actor>	<type>	<from>	<to>
...
HISTORY_END
```

Truncation behavior is controlled by flags:
- `--max-description-chars <n>` (default 4000).
- `--max-comment-chars <n>` (default 500).

#### 5.2.3 Create and Update Issues

- `ltui issues create [options...]`
  - `--team <key>` (default from `.ltui.json:teamKey` if present)
  - `--project <key-or-id>` (default from `.ltui.json:projectId` if present)
  - `--title <string>`
  - `--description <string-or-@path>`
  - `--state <name-or-id>` (default from `.ltui.json:defaultIssueState` if present)
  - `--label <name-or-id>` (repeatable; defaults merged with `.ltui.json:defaultLabels` if present)
  - `--assignee <me|email|id>` (default from `.ltui.json:defaultAssignee` if present)
  - `--priority <0-4>`
  - Output: a single `ISSUE_CREATED` block in `detail` format.

- `ltui issues update <issue-id-or-key> [options...]`
  - Same fields as `create`, but all optional.
  - Also:
    - `--state <name-or-id>` (for changing issue state)
    - `--add-label <name-or-id>` (repeatable)
    - `--remove-label <name-or-id>` (repeatable)
    - `--estimate <number>`
    - `--due <iso>`
  - Output: `ISSUE_UPDATED` detail block.

#### 5.2.4 Comments and Links

- `ltui issues comment <issue-id-or-key> --body <text-or-@path>`
  - Adds a comment.
  - Output: `COMMENT_CREATED` block with id, author, timestamps.

- `ltui issues link <issue-id-or-key> --url <url> [--title <title>]`
  - Attaches a link (e.g. PR, build, docs).
  - Output: `LINK_ATTACHED` block.

#### 5.2.5 Relationships

- `ltui issues relate <child> --parent <parent>`
  - Sets parent/child relationship.

- `ltui issues block <issue> --blocked-by <other-issue>`
  - Adds blocking relationship.

Output: `RELATIONSHIP_UPDATED` block summarizing change.

### 5.3 Teams

- `ltui teams list`
  - Lists teams in TSV format:

  ```text
  id	key	name	default_assignee	active
  <id>	<key>	<name>	<default-assignee-or-none>	<true/false>
  ```

- `ltui teams view <key-or-id>`
  - Shows detail view including default workflow states.

### 5.4 Projects

- `ltui projects list [--team <key-or-id>] [--state <state>]`
  - TSV with project metadata relevant to bugfix context (state, target date).

- `ltui projects view <id-or-key>`
  - Detail view with milestones and linked issues (summary only).

- `ltui projects align <id-or-key> [options...]`
  - Writes/updates `.ltui.json` in the current directory to align this repo with a Linear project/team.
  - Options:
    - `--profile <name>` – set project‑specific profile.
    - `--team <key-or-id>` – set default team.
    - `--state <name>` – set `defaultIssueState`.
    - `--label <name>` (repeatable) – set `defaultLabels`.
    - `--assignee <me|email|id>` – set `defaultAssignee`.
  - Output: `PROJECT_ALIGNED` detail block summarizing effective `.ltui.json` values.

### 5.5 Cycles, Labels, Users

Provide similar minimal but consistent surfaces:

- `ltui cycles list [--team <key-or-id>]`
  - Fields: `id`, `number`, `name`, `startsAt`, `endsAt`, `status`.

- `ltui labels list [--team <key-or-id>]`
  - Fields: `id`, `name`, `group`, `color`.

- `ltui users list [--active-only]`
  - Fields: `id`, `name`, `email`, `displayName`.

---

## 6. Output Contracts and Token Efficiency

### 6.1 General Rules

- **No ANSI escape sequences** by default in any mode.
- **No extraneous prose** in agent mode (no sentences, only headers/rows).
- All headers are **UPPERCASE_WITH_UNDERSCORES** and stable.
- Values never include tabs or newlines in TSV rows; multi‑line content is wrapped in explicit `*_START` / `*_END` sections.
- JSON output is compact (`space: 0`, `no pretty print`).

### 6.2 Error Format

On non‑zero exit, the first line is:

```text
ERROR: <code> <short-message>
```

Followed by optional detail lines, e.g.:

```text
ERROR: auth_missing No API key configured for profile 'personal'
HINT: Run 'ltui auth add --profile personal --api-key <key>'
```

Error codes (initial set):
- `auth_missing`
- `auth_invalid`
- `api_error`
- `not_found`
- `validation_error`
- `network_error`
- `unknown`

### 6.3 Pagination

List commands that support pagination include cursor metadata in agent mode:

```text
CURSOR_NEXT: <cursor-or-empty>
CURSOR_PREV: <cursor-or-empty>
COUNT: <n-returned>
```

These lines appear **before** the header row.

### 6.4 Field Selection

- `--fields` applies to `table` and `tsv` formats.
- Values outside the supported set are rejected with `validation_error`.
- Each command defines its own allowed field names (documented in `--help`).

Example:

```bash
ltui issues list --fields identifier,title,state
```

Produces TSV header:

```text
identifier	title	state
...
```

### 6.5 Truncation and Summaries

To keep outputs within token budgets:

- Description and comment bodies are truncated at configurable char limits.
- A truncation is indicated by a trailing `…` and an extra line:

```text
DESCRIPTION_TRUNCATED: true
```

- `--summary-only` flags can be added (e.g. `issues view`) to omit long bodies entirely.

---

## 7. Linear SDK Integration

### 7.1 Client Construction

Central module `src/client.ts`:

- Resolves profile and API key (honoring env overrides).
- Constructs a single `LinearClient` instance per process.
- Handles:
  - Pagination (wrapping SDK pagination utilities).
  - Basic retry on transient errors (HTTP 5xx, network).

### 7.2 Mapping to SDK Operations

- Use the strongly‑typed operations from `@linear/sdk`:
  - Issues: `client.issue`, `client.issues`, `client.issueCreate`, `client.issueUpdate`, `client.commentCreate`, etc.
  - Teams: `client.teams`, `client.team`.
  - Projects: `client.projects`, `client.project`.
  - Cycles: `client.cycles`.
  - Labels: `client.issueLabels`.
  - Users: `client.users`, `client.viewer`.

Where the SDK exposes higher‑level helpers (e.g. by key or identifier), prefer those over raw IDs to keep the interface natural.

### 7.3 Rate Limiting and Performance

- Respect Linear API rate limits:
  - Limit concurrency for bulk operations.
  - Surface rate limit errors clearly with `ERROR: api_error rate_limited`.
- Optionally cache stable lookups (e.g. team key → id, label name → id) in memory per process, and on disk in `~/.config/ltui/cache.json` with short TTL.

---

## 8. Directory Structure

Proposed repository layout:

```text
.
├── bin/
│   └── ltui               # Node.js entrypoint (shebang)
├── src/
│   ├── cli.ts             # CLI bootstrap and command registration
│   ├── client.ts          # LinearClient construction and helpers
│   ├── config.ts          # Profiles, config file I/O
│   ├── format.ts          # Common formatting utilities (TSV, detail, JSON)
│   ├── commands/
│   │   ├── issues.ts
│   │   ├── teams.ts
│   │   ├── projects.ts
│   │   ├── cycles.ts
│   │   ├── labels.ts
│   │   ├── users.ts
│   │   └── auth.ts
├── package.json
├── tsconfig.json
└── README.md
```

---

## 9. Usage Examples (Agent‑Oriented)

### 9.1 Find Relevant Issues for a Bug

```bash
# List recent issues in the ENGINEERING team labeled "bug"
ltui issues list --team ENG --label bug --limit 30 --agent
```

### 9.2 Inspect a Single Issue with Comments

```bash
ltui issues view ENG-123 --include-comments --agent --max-description-chars 2000
```

### 9.3 Update Status and Add a Comment

```bash
ltui issues update ENG-123 --state "In Progress" --assignee me --agent
ltui issues comment ENG-123 --body "Working on this as part of bugfix branch feature/fix-ENG-123" --agent
```

### 9.4 Attach a Pull Request Link

```bash
ltui issues link ENG-123 --url "https://github.com/org/repo/pull/456" --title "PR #456" --agent
```

### 9.5 Per‑Project Alignment + Issue Creation

```bash
# Align the current repo with a Linear project and defaults
ltui projects align ENG-ROADMAP --team ENG --state "Todo" --label bug --label backend --assignee me --agent

# Create a new issue in this repo; team/project/state/labels/assignee come from .ltui.json
ltui issues create --title "Fix crash on startup" --description @docs/crash-notes.md --agent
```

---

## 10. Roadmap

Short‑term:
- Implement `auth`, `issues`, `teams`, `projects`, `cycles`, `labels`, `users` commands.
- Ship agent‑mode output contracts as described here.
- Add tests for each command’s output format.

Medium‑term:
- Enhanced search and saved queries.
- Better integration with VCS tools (passing branch/commit information as links).

Long‑term:
- Additional API coverage (notifications, documents, roadmaps, milestones).
- Pluggable extensions for org‑specific workflows.
- Optional persistent local cache to reduce repeated network requests.
