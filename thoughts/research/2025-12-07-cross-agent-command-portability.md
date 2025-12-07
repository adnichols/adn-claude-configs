---
date: 2025-12-07T18:57:34Z
author: claude
git_commit: 585872a4dd971d2acb9b590569fb79eac186cfd6
branch: main
repository: adn-claude-configs
type: research
status: complete
tags: [cross-platform, commands, agents, claude-code, codex, gemini-cli, configuration]
last_updated: 2025-12-07
---

# Research: Cross-Agent Command Portability for Claude Code, Codex, and Gemini CLI

## Research Question

How to make commands available to agents that aren't aware of the `.claude` directory, with an approach to installing commands to a location that's accessible while making them work properly with Claude Code, Gemini CLI, and Codex. Also supporting ltui (Linear) integration into GEMINI.md.

## Summary

All three AI CLI tools (Claude Code, Codex, and Gemini CLI) support custom commands/prompts with similar concepts but different implementation details. A unified approach is possible by:

1. **Shared source of truth**: Maintain commands in a canonical format (Markdown with YAML front-matter)
2. **Format converters**: Build converters to transform commands to each platform's native format
3. **Unified installation**: Extend `install.sh` to install to all three platforms' expected locations
4. **Platform-specific context files**: Generate CLAUDE.md, CODEX.md, and GEMINI.md appropriately

## Detailed Findings

### Platform Comparison Matrix

| Feature | Claude Code | Codex | Gemini CLI |
|---------|-------------|-------|------------|
| **Command Format** | Markdown (`.md`) with YAML front-matter | Markdown (`.md`) with YAML front-matter | TOML (`.toml`) |
| **Project Location** | `.claude/commands/` | Removed (global only) | `.gemini/commands/` |
| **Global Location** | `~/.claude/commands/` | `~/.codex/prompts/` | `~/.gemini/commands/` |
| **Namespacing** | Colon-delimited in filename | Colon-delimited in filename | Subdirectories → colons |
| **Arguments** | `$ARGUMENTS` placeholder | `$ARGUMENTS` placeholder | `{{args}}` placeholder |
| **Shell Execution** | N/A (uses Bash tool) | N/A (uses Bash tool) | `!{command}` syntax |
| **Context File** | `CLAUDE.md` | `CODEX.md` (auto-generated) | `GEMINI.md` |
| **Agent Definition** | `.claude/agents/*.md` | References CLAUDE.md agents | Not natively supported |
| **Settings Format** | JSON (`settings.local.json`) | TOML (`config.toml`) | JSON (`settings.json`) |
| **MCP Servers** | JSON (`mcp-servers.json`) | TOML (`[mcp_servers.*]`) | JSON in settings.json |

### Claude Code Configuration

**File Locations:**
- Project: `<project>/.claude/`
- Global: `~/.claude/`

**Command Structure (`claude/commands/spec:1:create-spec.md:1-4`):**
```yaml
---
description: Research an idea and produce a specification document
argument-hint: [Idea/Feature Description]
---
```

**Agent Structure (`claude/agents/developer-fidelity.md:1-6`):**
```yaml
---
name: developer-fidelity
description: Implements specifications with absolute fidelity
model: sonnet
color: blue
---
```

**Key Patterns:**
- Commands use `$ARGUMENTS` for user input
- Agents referenced with `@agent-name` syntax in commands
- Commands can invoke agents: `@developer-fidelity`
- All agents check CLAUDE.md for project-specific standards
- Flat file structure with colon-delimited namespacing

### Codex Configuration

**File Locations:**
- Project: `<project>/.codex/config.toml` and `mcp-servers.toml`
- Global: `~/.codex/prompts/` and `~/.codex/scripts/`

**Command Structure (identical to Claude Code):**
```yaml
---
description: Process tasks in a task list with fidelity-preserving agent selection
argument-hint: [Files]
---
```

**Key Differences:**
- Prompts installed globally only (`~/.codex/prompts/`)
- Project `.codex/prompts/` and `.codex/scripts/` are removed during install
- Uses TOML for configuration (`config.toml`)
- Model: `gpt-5-codex` vs Claude's `sonnet`
- `approval_policy = "never"` for autonomous execution

### Gemini CLI Configuration

**File Locations:**
- Project: `<project>/.gemini/commands/` and `.gemini/settings.json`
- Global: `~/.gemini/commands/` and `~/.gemini/settings.json`

**Command Structure (TOML format):**
```toml
description = "Research an idea and produce a specification document"
prompt = """
# Rule: Research and Generate Specification Document

## Goal
...

Consider any input from {{args}}
...
"""
```

**Key Patterns:**
- Uses `{{args}}` instead of `$ARGUMENTS`
- Supports shell command execution with `!{git diff --staged}` syntax
- Subdirectory structure becomes colon namespacing: `git/commit.toml` → `/git:commit`
- GEMINI.md provides project context (hierarchical: global → project → subdirs)
- No native agent concept (must be embedded in GEMINI.md or commands)

## Architecture for Cross-Platform Support

### Proposed Directory Structure

```
adn-claude-configs/
├── source/                     # Canonical source of truth
│   ├── commands/               # Universal command definitions
│   │   ├── spec/
│   │   │   └── create-spec.md  # Markdown with universal metadata
│   │   ├── prd/
│   │   │   └── create-prd.md
│   │   └── ...
│   ├── agents/                 # Agent definitions (for platforms that support them)
│   │   └── developer-fidelity.md
│   └── context/                # Context file templates
│       ├── CLAUDE.template.md
│       ├── GEMINI.template.md
│       └── CODEX.template.md
│
├── claude/                     # Claude Code output (current structure)
│   ├── commands/               # Generated from source/commands/
│   ├── agents/                 # Copy of source/agents/
│   └── ...
│
├── codex/                      # Codex output (current structure)
│   ├── prompts/                # Generated from source/commands/
│   └── ...
│
├── gemini/                     # NEW: Gemini CLI output
│   ├── commands/               # Generated TOML from source/commands/
│   └── GEMINI.template.md      # Context template with ltui integration
│
├── scripts/
│   └── build-commands.py       # Converts source/ to platform-specific formats
│
└── install.sh                  # Extended to support --gemini flag
```

### Universal Command Format

A new universal markdown format that can be converted to all platforms:

```markdown
---
# Universal metadata
description: Research an idea and produce a specification document
argument-hint: [Idea/Feature Description]

# Platform-specific overrides (optional)
claude:
  model: sonnet
gemini:
  approval-mode: default
codex:
  model: gpt-5-codex
---

# Rule: Research and Generate Specification Document

## Goal

To guide an AI assistant in researching a user's idea...

## Input

Consider any input from {{ARGS}}

<!-- The {{ARGS}} placeholder gets converted to:
     - $ARGUMENTS for Claude Code and Codex
     - {{args}} for Gemini CLI
-->
```

### Conversion Rules

**Claude Code / Codex:**
- Keep filename structure: `spec/create-spec.md` → `spec:1:create-spec.md`
- Replace `{{ARGS}}` → `$ARGUMENTS`
- Keep YAML front-matter with `description` and `argument-hint`

**Gemini CLI:**
- Convert to TOML: `spec/create-spec.md` → `spec/create-spec.toml`
- Replace `{{ARGS}}` → `{{args}}`
- Move content to `prompt = """..."""` field
- Add `description = "..."` from YAML

### Agent Handling Across Platforms

**Claude Code:**
- Native support via `.claude/agents/*.md`
- Commands reference with `@agent-name`

**Codex:**
- No native agent support
- Agents embedded as instructions in prompts
- Can reference AGENTS.md for project-level agent documentation

**Gemini CLI:**
- No native agent support
- Agents embedded in GEMINI.md as "personas" or "modes"
- Commands can include agent instructions inline

**Proposed Solution:**
For Gemini CLI, convert agent definitions to a "Persona" section in GEMINI.md:

```markdown
# GEMINI.md

## Available Personas

When a command specifies a persona, adopt that role completely.

### @developer-fidelity
You are a Developer who implements specifications with absolute fidelity...
[Full agent content embedded]

### @quality-reviewer
You review code for production issues...
[Full agent content embedded]
```

### GEMINI.md with ltui Integration

```markdown
# Project Context

[Project-specific instructions...]

## Linear Integration (ltui)

This project uses the `ltui` CLI tool for Linear integration.

### Setup

1. Obtain Linear API Key from linear.app/settings/api
2. Configure: `ltui auth add --name default --key <your-api-key>`
3. Verify: `ltui auth list`

### Common Commands

**View issue details:**
```bash
ltui issues view <ISSUE_KEY> --format detail
```

**Update issue state:**
```bash
ltui issues update <ISSUE_KEY> --state "In Review"
```

**Add a comment:**
```bash
ltui issues comment <ISSUE_KEY> --body "Comment text"
```

[Additional ltui documentation...]

## Available Personas

### @developer-fidelity
[Embedded agent instructions...]

### @quality-reviewer-fidelity
[Embedded agent instructions...]
```

### Installation Changes

Extend `install.sh` with `--gemini` flag:

```bash
# New installation options
./install.sh --claude            # Claude Code only
./install.sh --codex             # Codex only
./install.sh --gemini            # Gemini CLI only
./install.sh --all               # All three platforms

# Target directory support
./install.sh --gemini ~/project  # Install Gemini to specific project
./install.sh --gemini ~          # Install Gemini globally
```

**Gemini Installation Steps:**
1. Create `<target>/.gemini/commands/` if not exists
2. Copy TOML command files from `gemini/commands/`
3. Merge/create GEMINI.md with ltui integration
4. Merge settings.json with MCP server configurations (if any)

## Code References

| File | Lines | Description |
|------|-------|-------------|
| `install.sh` | 561-648 | `install_claude()` function |
| `install.sh` | 728-802 | `install_codex()` function |
| `install.sh` | 183-222 | ltui integration section |
| `claude/commands/spec:1:create-spec.md` | 1-4 | Command YAML front-matter |
| `claude/agents/developer-fidelity.md` | 1-6 | Agent YAML front-matter |
| `codex/prompts/spec:1:create-spec.md` | 1-4 | Codex prompt format |

## Architecture Documentation

### Format Conversion Pipeline

```
source/commands/spec/create-spec.md
    │
    ├─── [claude converter] ──→ claude/commands/spec:1:create-spec.md
    │                           (Markdown, $ARGUMENTS)
    │
    ├─── [codex converter] ───→ codex/prompts/spec:1:create-spec.md
    │                           (Markdown, $ARGUMENTS)
    │
    └─── [gemini converter] ──→ gemini/commands/spec/create-spec.toml
                                (TOML, {{args}})
```

### Context File Strategy

| Platform | File | Generation Strategy |
|----------|------|---------------------|
| Claude Code | CLAUDE.md | Manual (not installed, project-specific) |
| Codex | CODEX.md | Auto-generated by Codex |
| Gemini CLI | GEMINI.md | Template + ltui + embedded agents |

### MCP Server Portability

All three platforms support MCP servers with different configuration formats:

**Claude Code (JSON):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**Codex (TOML):**
```toml
[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]
```

**Gemini CLI (JSON in settings.json):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

## Related Documents

- CLAUDE.md (repository root) - Current Claude Code configuration
- claude/commands/README.md - Command documentation
- codex/README.md - Codex configuration documentation

## Decisions Made

1. **Maintain Separate Gemini Versions**: Commands will be maintained as separate TOML files in `gemini/commands/`, not converted at install time. This allows platform-specific optimizations.

2. **Use Personas for Agents**: Agents will be embedded in GEMINI.md as "Personas" following Gemini's canonical patterns. Commands can reference personas with `@persona-name` syntax in prompts.

3. **Flat Namespace with Colons**: Use flat filenames with colons matching Claude/Codex pattern: `prd:1:create-prd.toml`. Gemini CLI supports colons in filenames.

## Remaining Considerations

1. **Sync Strategy**: When Claude/Codex commands change, Gemini versions need manual updates. Consider a diff tool to identify drift.

2. **Shell Execution Parity**: Gemini's `!{command}` syntax allows inline shell execution. Claude/Codex use the Bash tool. Commands should be written to work with each platform's native approach.

## Implementation Recommendations

### Phase 1: Gemini CLI Support

1. **Create `gemini/` directory structure:**
   ```
   gemini/
   ├── commands/                    # TOML command files (flat with colons)
   │   ├── spec:1:create-spec.toml
   │   ├── prd:1:create-prd.toml
   │   ├── 3:process-tasks.toml
   │   └── ...
   ├── GEMINI.template.md           # Context template with personas + ltui
   └── settings.json                # MCP server config (optional)
   ```

2. **Convert priority commands to TOML:**
   - `spec:1:create-spec.toml`
   - `prd:1:create-prd.toml`
   - `3:process-tasks.toml`
   - `cmd:start-linear-issue.toml`

3. **Create GEMINI.template.md with:**
   - ltui integration section (from current CLAUDE.md)
   - Personas section with embedded agents
   - Project context patterns

4. **Extend install.sh:**
   - Add `--gemini` flag
   - Install to `<target>/.gemini/commands/`
   - Merge/create GEMINI.md from template

### Phase 2: Full Command Coverage

1. Convert remaining commands to TOML format
2. Document command parity across platforms
3. Add sync check script to identify drift

### Phase 3: Maintenance Tooling

1. Create `scripts/check-command-sync.sh` to compare command coverage
2. Add documentation for adding new commands across all platforms
