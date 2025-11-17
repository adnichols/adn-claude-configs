# ltui — Linear CLI for AI Coding Agents

`ltui` is a token-efficient command-line interface to Linear, purpose-built for AI coding agents like Claude Code, Cursor, Aider, and similar tools. Unlike traditional CLIs designed for human interaction, ltui prioritizes **deterministic output**, **minimal token usage**, and **structured data formats** that LLMs can reliably parse.

## Why ltui Exists

When AI agents work on codebases, they often need to interact with Linear to:
- Find and read issue details
- Update issue status as work progresses
- Add comments linking PRs and commits
- Create new issues for discovered bugs or follow-up work
- Manage labels, assignments, and project membership

Existing Linear tools are designed for humans and produce:
- Colorful, formatted output with ANSI escape codes (wastes tokens)
- Inconsistent output formats (hard for LLMs to parse reliably)
- Interactive prompts (incompatible with non-interactive agent workflows)
- Verbose descriptions and redundant data

**ltui solves this** by providing a deterministic, parseable CLI interface optimized for machine consumption while remaining human-readable enough for you to debug and understand what your agent is doing.

## Key Design Principles

### 1. Token Efficiency
Output defaults to **TSV (tab-separated values)** format, which conveys the same information as JSON or verbose text using 50-70% fewer tokens. Every token counts when working within LLM context windows.

### 2. Deterministic Output
Same command + same Linear state = **identical byte-for-byte output**. No timestamps, no random ordering, no environmental dependencies. Agents can cache and reliably parse results.

### 3. Structured Errors
Errors follow a predictable format with error codes and hints:
```
ERROR: not_found Issue ENG-123 not found
HINT: Check the issue ID or use 'ltui issues list' to find available issues
```

Agents can programmatically detect and handle specific error conditions.

### 4. No Interactivity
All inputs via CLI flags or environment variables. No prompts, no confirmations, no interactive flows. Perfect for scripted agent workflows.

### 5. Multi-Workspace Support
Configure profiles for different Linear workspaces. Agents can work across personal projects, work projects, and client projects by switching profiles.

## Installation

### Prerequisites
- Node.js ≥ 20.0.0 (or Bun)
- A Linear account with API access

### Quick Install (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ltui

# Run the installer (builds, links globally, and installs Claude Code skill)
./install.sh
```

This will:
1. Install dependencies and build the project
2. Link `ltui` globally so it's available system-wide
3. Install the Claude Code skill to `~/.claude/skills/ltui.md`

After installation:
- Run `ltui --help` from anywhere to use the CLI
- Claude Code will automatically understand how to use ltui when working with Linear

### Manual Install

```bash
# Clone the repository
git clone <repository-url>
cd ltui

# Install dependencies (using Bun or npm)
bun install
# or: npm install

# Build the TypeScript source
bun run build
# or: npm run build

# Link globally for system-wide access
bun link
# or: npm link

# Optionally install Claude Code skill
mkdir -p ~/.claude/skills
cp claude/skills/ltui.md ~/.claude/skills/ltui.md
```

After linking, `ltui` will be available globally. Otherwise, use `./bin/ltui` from the project directory.

## Configuration

### 1. Get Your Linear API Key

1. Visit [Linear Settings → API](https://linear.app/settings/api)
2. Generate a new Personal API Key
3. Copy the key (starts with `lin_api_`)

### 2. Configure ltui

You have two options:

#### Option A: Environment Variable (Simplest)
```bash
export LINEAR_API_KEY="lin_api_..."
```

Add this to your agent's environment or shell profile. This is the easiest approach for single-workspace setups.

#### Option B: Profile-Based Configuration (Multi-Workspace)
```bash
# Add a named profile
ltui auth add personal

# When prompted, paste your API key
# This stores the key in ~/.config/ltui/profiles.json

# Set as default profile
ltui auth set-default personal
```

For multiple workspaces (e.g., work and personal):
```bash
ltui auth add work
ltui auth add personal
ltui auth set-default work

# Use --profile flag to switch contexts
ltui issues list --profile personal
```

### 3. Test Your Configuration

```bash
# List your Linear teams
ltui teams list

# Expected output (TSV format):
# TEAM: id	key	name
# 550e8400-...	ENG	Engineering
# 550e8401-...	PROD	Product
```

If you see your teams, you're ready to go!

## Per-Project Alignment (Recommended for Agents)

When working on a codebase tied to a specific Linear project, create a `.ltui.json` file in your repository root:

```bash
# From your project directory
ltui projects align

# This prompts for:
# - Which Linear team this repo belongs to
# - Which Linear project to use by default
# - Default labels for new issues (optional)
# - Default assignee (optional)

# Saves to ./.ltui.json
```

**Example `.ltui.json`:**
```json
{
  "profile": "work",
  "team": "ENG",
  "project": "Backend Services",
  "labels": ["backend", "api"],
  "assignee": "me",
  "state": "In Progress"
}
```

Now when your agent runs commands from this directory, it automatically uses these defaults:
```bash
# Without .ltui.json - requires many flags
ltui issues create --team ENG --project "Backend Services" --labels backend,api --title "Fix auth bug"

# With .ltui.json - just provide the unique bits
ltui issues create --title "Fix auth bug"
```

**💡 Commit `.ltui.json` to your repository** so all agents and developers share the same Linear project alignment.

## Output Formats

ltui supports four output formats via the `--format` flag:

### TSV (Default for Agents)
```bash
ltui issues list --format tsv
```
```
ISSUE: id	identifier	title	state	assignee
550e8400-...	ENG-123	Fix login bug	In Progress	alice@example.com
550e8401-...	ENG-124	Add logging	Todo	bob@example.com
```

**Best for:** Agent parsing, minimal token usage, grep/awk processing

### Table (Human-Readable)
```bash
ltui issues list --format table
```
```
ID                                    IDENTIFIER  TITLE           STATE         ASSIGNEE
550e8400-e29b-41d4-a716-446655440000  ENG-123     Fix login bug   In Progress   alice@example.com
550e8401-e29b-41d4-a716-446655440001  ENG-124     Add logging     Todo          bob@example.com
```

**Best for:** Human review, debugging agent behavior

### Detail (Full Context)
```bash
ltui issues view ENG-123 --format detail
```
```
ISSUE: ENG-123
TITLE: Fix authentication regression in OAuth flow
STATE: In Progress
ASSIGNEE: alice@example.com
LABELS: bug, security, backend
CREATED: 2024-01-15T10:30:00Z
UPDATED: 2024-01-16T14:22:00Z

DESCRIPTION_START
The OAuth callback handler is returning 500 errors for GitHub login attempts.
Error occurs in production but not staging.
DESCRIPTION_END

COMMENTS_START
COMMENT: bob@example.com 2024-01-16T09:15:00Z
Traced to session cookie domain mismatch. Fix in PR #234.

COMMENT: alice@example.com 2024-01-16T14:22:00Z
Confirmed fix works. Deploying to prod.
COMMENTS_END
```

**Best for:** Full issue context, agents needing complete information

### JSON (Machine-Readable)
```bash
ltui issues list --format json
```
```json
{"issues":[{"id":"550e8400-...","identifier":"ENG-123","title":"Fix login bug","state":"In Progress","assignee":"alice@example.com"}]}
```

**Best for:** Structured parsing, integration with other tools

## Common Agent Workflows

### Workflow 1: Creating an Issue from Code Discovery

```bash
# Agent discovers a bug while working on feature X
ltui issues create \
  --title "Memory leak in background worker" \
  --description "Found while implementing feature X. Worker process grows 10MB/hour." \
  --labels bug,performance \
  --priority 2 \
  --state "Backlog"

# Output:
# ISSUE: ENG-456
# URL: https://linear.app/team/issue/ENG-456
```

Agent can store `ENG-456` and reference it in commit messages or PR descriptions.

### Workflow 2: Updating Status as Work Progresses

```bash
# Agent starts work on assigned issue
ltui issues update ENG-123 --state "In Progress"

# Agent completes implementation
ltui issues update ENG-123 --state "In Review"

# Agent adds PR link
ltui issues comment ENG-123 "Implementation complete in PR #234"
ltui issues link ENG-123 https://github.com/org/repo/pull/234
```

### Workflow 3: Finding Relevant Issues

```bash
# Find all "bug" issues in "Todo" state
ltui issues list --label bug --state Todo --format tsv

# Find issues assigned to me that are in progress
ltui issues list --assignee me --state "In Progress" --format tsv

# Search issue titles for specific keywords
ltui issues list --query "authentication" --format tsv
```

### Workflow 4: Reading Full Issue Context

```bash
# Get complete issue details including description and comments
ltui issues view ENG-123 --format detail

# Agent parses DESCRIPTION_START...DESCRIPTION_END and COMMENTS_START...COMMENTS_END blocks
```

## Caching and Performance

ltui caches Linear entity lookups (teams, projects, labels, users) to minimize API calls:
- **In-memory cache:** Valid for the command's lifetime
- **Disk cache:** `~/.config/ltui/cache.json`, 5-minute TTL
- **Cache invalidation:** Automatic based on TTL

When agents repeatedly query the same entities (e.g., "What's the ID of the Engineering team?"), the cache prevents redundant API calls, saving time and respecting rate limits.

To clear the cache manually:
```bash
rm ~/.config/ltui/cache.json
```

## Extending ltui for Your Workflow

Place custom commands in `~/.config/ltui/extensions/`:

```javascript
// ~/.config/ltui/extensions/my-workflow.js
export function register(program) {
  program
    .command('my-workflow:standup')
    .description('Generate standup summary for assigned issues')
    .action(async () => {
      // Your custom logic using Linear SDK
    });
}
```

Extensions are auto-loaded at runtime. See `src/extensions.ts` for the extension API.

## Testing and Validation

```bash
# Run full test suite
bun run test

# Tests include:
# - CLI argument validation (--help output for all commands)
# - End-to-end regression tests using mock Linear client
# - Output format contract validation
```

Tests use a mock Linear client (`src/test-utils/mockLinearClient.ts`) to ensure deterministic behavior without network calls.

## Troubleshooting

### "ERROR: auth_missing No API key configured"
- Set `LINEAR_API_KEY` environment variable, OR
- Run `ltui auth add <profile-name>` and configure a profile

### "ERROR: not_found Team not found"
- Verify team key/name with `ltui teams list`
- Check that you're using the correct profile (`--profile` flag)

### "ERROR: api_error Rate limit exceeded"
- Linear API has rate limits (check Linear docs for current limits)
- ltui's cache reduces API calls, but very high-frequency usage may hit limits
- Wait 60 seconds and retry

### Unexpected Output Format
- Verify `--format` flag (defaults to `tsv`)
- Check that `LTUI_AGENT_MODE` is not set to `0` (agent mode is enabled by default)

## Agent Integration Tips

### For Claude Code
`ltui` includes a built-in skill for Claude Code that teaches the AI assistant how to effectively use ltui to interact with Linear.

**Installation:**
The skill is automatically installed when you run `./install.sh`, or manually:
```bash
mkdir -p ~/.claude/skills
cp claude/skills/ltui.md ~/.claude/skills/ltui.md
```

**What the skill provides:**
- Complete command reference and examples
- Best practices for token-efficient usage
- Common workflows (creating issues, updating status, managing relationships)
- Output format parsing guidance
- Error handling patterns

Once installed, Claude Code will automatically understand how to:
- Check Linear issues, projects, and teams
- Create and update issues with proper formatting
- Add comments and links to issues
- Manage issue relationships and labels
- Parse ltui output efficiently

**Usage:**
Just ask Claude naturally: "Check my Linear issues" or "Create a Linear issue for this bug" and Claude will use ltui automatically.

### For MCP Servers
If you're setting this up for an MCP server integration:

1. **Set up a dedicated profile** for the agent with appropriate Linear API key permissions
2. **Create `.ltui.json`** in each project repository for automatic context alignment
3. **Use TSV format** in prompts to minimize token usage
4. **Parse structured errors** to handle failure cases gracefully
5. **Cache issue IDs** in agent memory to avoid repeated lookups

### For Cursor / Aider / Other Agents
Same principles apply:
- Configure authentication once globally
- Use per-project `.ltui.json` for automatic defaults
- Prefer TSV output for parsing
- Handle structured errors programmatically
- Consider copying `claude/skills/ltui.md` to your agent's skill/documentation directory

## Project Structure

```
ltui/
├── bin/ltui              # CLI entrypoint
├── src/
│   ├── cli.ts            # Command registration and parsing
│   ├── client.ts         # Linear client initialization
│   ├── config.ts         # Profile and config management
│   ├── linear.ts         # Entity resolution (teams, projects, etc.)
│   ├── format.ts         # Output formatting (TSV, table, detail, JSON)
│   ├── cache.ts          # Disk and in-memory caching
│   ├── queries.ts        # Reusable GraphQL fragments
│   ├── extensions.ts     # User extension loader
│   └── commands/         # Command implementations
│       ├── auth.ts       # Profile management
│       ├── issues.ts     # Issue operations
│       ├── teams.ts      # Team listing
│       ├── projects.ts   # Project operations
│       ├── cycles.ts     # Cycle queries
│       ├── labels.ts     # Label management
│       └── users.ts      # User queries
├── claude/
│   └── skills/
│       └── ltui.md       # Claude Code skill definition
├── install.sh            # Installation script
├── SPEC.md               # Full technical specification
├── AGENTS.md             # Development guidelines
├── CLAUDE.md             # Instructions for Claude Code
└── README.md             # This file
```

## Additional Resources

- **[SPEC.md](./SPEC.md)** — Complete technical specification with API contracts
- **[AGENTS.md](./AGENTS.md)** — Development and testing guidelines
- **[Linear API Documentation](https://developers.linear.app/)** — Official Linear API reference

## License

[Add license information]

## Contributing

Contributions welcome! Please read [AGENTS.md](./AGENTS.md) for development guidelines and testing requirements.

---

**Built for AI agents, readable by humans.**
