# Claude Code Configuration

This directory contains installable Claude Code configurations including agents, commands, and settings.

## Contents

- **agents/** - Specialized AI agents for different tasks
- **commands/** - Custom slash commands for workflows
- **scripts/** - Shared utility scripts used by commands
- **settings.local.json** - Claude Code project-level settings
- **mcp-servers.json** - MCP (Model Context Protocol) server definitions

## Installation

### To a New Project

```bash
cd /path/to/your/project
bash /path/to/adn-claude-configs/install.sh --claude
```

### To Your Home Directory

```bash
bash /path/to/adn-claude-configs/install.sh --claude ~
```

This will copy all configurations to `~/.claude/` for global access.

## MCP Servers

The `mcp-servers.json` file contains MCP server configurations. To use these servers:

1. **For Claude Desktop App**: Merge contents into:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **For Claude Code**: The servers are automatically available when installed in a project's `.claude/` directory. Ensure your global Claude Code settings have:
   ```json
   {
     "enableAllProjectMcpServers": true
   }
   ```

### Example MCP Server Configuration

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

## Settings

The `settings.local.json` file contains:
- **permissions**: Tool access controls
- **model**: Default model selection

Customize these settings for your project's needs. The settings are merged with global Claude Code settings.

## Updating

To sync the latest agents, commands, and scripts from the adn-claude-configs repository:

```bash
cd /path/to/your/project
bash /path/to/adn-claude-configs/update.sh
```

This preserves your local `settings.local.json` while updating everything else.

## Available Agents

- **developer-fidelity**: Exact scope implementation with zero scope creep
- **quality-reviewer-fidelity**: Reviews against specifications only
- **debugger**: Systematic bug analysis
- **simplify-planner**: Code complexity reduction specialist
- **technical-writer**: Documentation creation

See individual agent files in `agents/` for detailed descriptions.

## Available Commands

- `/p:create-prd` - Create Product Requirements Documents
- `/p:spec-to-tasks` - Convert specifications to task lists
- `/b:process-tasks` - Execute tasks with fidelity preservation
- `/simplify:create-plan` - Generate code simplification plans
- `/docs:fetch` - Fetch library documentation

See individual command files in `commands/` for usage details.

## Notes

- **CLAUDE.md is NOT installed** - Codex generates this file based on your project
- Settings are merged with global Claude Code configuration
- MCP servers must be configured separately (see above)
