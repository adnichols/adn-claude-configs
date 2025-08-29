# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a Claude Code configuration repository containing:

- **agents/**: Custom agent definitions for specialized tasks (developer, quality-reviewer, simplify-planner, etc.)
- **commands/**: Custom slash commands for task processing and code management
- **settings.json**: Claude Code configuration with custom status line and MCP servers

## Custom Agents

Key specialized agents available:

- `developer`: Implements specs with tests - enforces zero linting violations
- `quality-reviewer`: Reviews code for production failures (security, data loss, performance)
- `simplify-planner`: Code cleanup specialist for complexity reduction
- `debugger`: Systematic bug analysis through evidence gathering
- `technical-writer`: Creates documentation after feature completion

## Custom Commands

Important slash commands:

- `/user:add-command`: Create new personal slash commands in ~/.claude/commands
- `/build:process-tasks`: Process task lists with git branch management and test requirements
- `/simplify:create-plan`: Generate code simplification plans using simplify-planner agent
- `/simplify:process-plan`: Execute existing simplification plans

## Configuration Notes

- Uses "sonnet" model as default
- MCP server "basic-memory" is configured for persistent memory
- Custom status line shows current directory and git branch with status
- Repository follows symlink pattern: .claude directory should link to .agents when copying

## Important Workflow Patterns

### Task Processing Requirements

When using `/build:process-tasks`:
- Must be on a git branch other than main
- One sub-task at a time (requires user confirmation unless NOSUBCONF specified)
- Test suite must pass before committing
- Follow conventional commit format with descriptive messages

### Code Simplification Workflow

1. Use `/simplify:create-plan` to analyze and plan
2. Quality review with @quality-reviewer agent
3. User approval required before implementation
4. Use `/simplify:process-plan` for execution

### Quality Standards

All agents reference CLAUDE.md for:
- Project-specific quality standards
- Error handling patterns
- Testing requirements
- Build and linting commands

When copying this repository setup to other projects, remember to recreate the .claude → .agents symlink structure.