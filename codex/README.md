# Codex Configuration

This directory contains installable Codex configurations including prompts, scripts, and settings.

## Contents

- **prompts/** - Custom prompt commands for workflows (equivalent to Claude Code commands)
- **scripts/** - Shared utility scripts used by prompts
- **config.toml** - Codex configuration template
- **mcp-servers.toml** - MCP (Model Context Protocol) server definitions

## Installation

### To a New Project

```bash
cd /path/to/your/project
bash /path/to/adn-claude-configs/install.sh --codex
```

### To Your Home Directory

```bash
bash /path/to/adn-claude-configs/install.sh --codex ~
```

This will copy all configurations to `~/.codex/` for global access.

## Configuration

### config.toml

The `config.toml` file contains Codex settings:

```toml
model = "gpt-5"
model_reasoning_effort = "high"

[cli]
default_cli_flags = [
  "--dangerously-bypass-approvals-and-sandbox",
  "--enable-web-search"
]

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]
```

If you already have a `config.toml`, the installer will preserve it. Review the new `config.toml` template and merge any new settings manually.

### MCP Servers

The `mcp-servers.toml` file contains additional MCP server configurations. To use these:

1. **Merge into ~/.codex/config.toml**: Copy the `[mcp_servers.*]` sections from `mcp-servers.toml` into your global or project-level `config.toml`

2. **Or use project-level**: Keep `mcp-servers.toml` separate and reference it in your project configuration

### Example MCP Server in config.toml

```toml
[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]

[mcp_servers.another-server]
command = "node"
args = ["/path/to/server.js"]
```

## Project Trust Levels

Codex requires projects to be marked as trusted. Add to your `~/.codex/config.toml`:

```toml
[projects."/path/to/your/project"]
trust_level = "trusted"
```

## Updating

To sync the latest prompts and scripts from the adn-claude-configs repository:

```bash
cd /path/to/your/project
bash /path/to/adn-claude-configs/update.sh
```

This preserves your local `config.toml` while updating prompts and scripts.

## Available Prompts

Codex uses prompts (similar to Claude Code's slash commands):

- `/p:create-prd` - Create Product Requirements Documents
- `/p:spec-to-tasks` - Convert specifications to task lists
- `/b:process-tasks` - Execute tasks with fidelity preservation
- `/b:process-tasks-codex` - Codex-specific task processing with autonomous execution
- `/simplify:create-plan` - Generate code simplification plans
- `/docs:fetch` - Fetch library documentation

See individual prompt files in `prompts/` for usage details.

## Differences from Claude Code

While the prompts are adapted from Claude Code commands, there are some differences:

1. **Format**: Codex uses the same markdown format for prompts
2. **Autonomous Execution**: `/b:process-tasks-codex` is designed for Codex's autonomous workflow
3. **Configuration**: Uses TOML instead of JSON
4. **Trust Model**: Requires explicit project trust levels

## Notes

- **CODEX.md is NOT installed** - Codex generates this file based on your project
- Configuration is merged with global Codex settings (`~/.codex/config.toml`)
- MCP servers must be configured in `config.toml` (see above)
