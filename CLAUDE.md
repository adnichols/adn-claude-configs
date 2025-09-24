# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a Claude Code configuration repository containing:

- **agents/**: Custom agent definitions for specialized tasks (developer, quality-reviewer, simplify-planner, etc.)
- **commands/**: Custom slash commands for task processing and code management
- **settings.json**: Claude Code configuration with custom status line and MCP servers

Note that when tools in this repository are used, they will be bind mounted into other code repos inside the .claude directory
ONLY the following directories will be available for use:

- commands/
- agents/
- scripts/

When used, these 3 directories will appear to be in these paths in another repo:

- .claude/commands/
- .claude/agents/
- .claude/scripts/

Other directories are local to this repository and will be unavailable when the tools are used.

The .claude directory in this repository is, in fact, a bind mounted example of how these commands present to other repos

## Custom Agents

Key specialized agents available:

- `developer`: Implements specs with tests - enforces zero linting violations
- `developer-fidelity`: Implements ONLY what's specified - no scope additions
- `quality-reviewer`: Reviews code for production failures (security, data loss, performance)
- `quality-reviewer-fidelity`: Reviews against specification requirements ONLY - prevents scope creep
- `simplify-planner`: Code cleanup specialist for complexity reduction
- `debugger`: Systematic bug analysis through evidence gathering
- `technical-writer`: Creates documentation after feature completion

## Custom Commands

Important slash commands:

- `/p:create-prd`: Create Product Requirements Documents with strict scope preservation
- `/p:gen-tasks`: Convert PRDs to task lists using fidelity-preserving approach
- `/p:spec-to-tasks`: Convert specifications directly to tasks with 100% fidelity
- `/b:process-tasks`: Process task lists with fidelity agents and git branch management
- `/simplify:create-plan`: Generate code simplification plans using simplify-planner agent
- `/simplify:process-plan`: Execute existing simplification plans
- `/docs:fetch`: Fetch documentation for a single library/framework
- `/docs:fetch-batch`: Batch fetch documentation from markdown lists containing multiple libraries
- `/user:add-command`: Create new personal slash commands in ~/.claude/commands

## Configuration Notes

- Uses "sonnet" model as default
- MCP server "basic-memory" is configured for persistent memory
- Custom status line shows current directory and git branch with status
- Repository follows symlink pattern: .claude directory should link to .agents when copying


## Available Documentation
- **Reactjs** (librarie): `docs/libraries/reactjs/` - 0% complete - *Updated 2025-08-31*


Fetched documentation available for enhanced Claude Code assistance:

- **Express** (framework): `docs/frameworks/express/` - 0% complete - *Updated 2025-08-31*
- **Lodash** (library): `docs/libraries/lodash/` - 0% complete - *Updated 2025-08-31*

## Important Workflow Patterns

### Task Processing Requirements

When using `/b:process-tasks`:

- Must be on a git branch other than main
- Uses fidelity-preserving agents (developer-fidelity, quality-reviewer-fidelity)
- One sub-task at a time (requires user confirmation unless NOSUBCONF specified)
- Test suite must pass before committing (only if tests were specified in source)
- Follow conventional commit format with descriptive messages
- Implement ONLY what's explicitly specified in source documents

### Fidelity-Preserving Workflow

All commands now follow the fidelity-preserving approach:

- **Exact Implementation**: Build only features explicitly specified in source documents
- **No Scope Expansion**: Zero additions beyond explicit requirements
- **Question Ambiguities**: Ask for clarification rather than making assumptions
- **Preserve Constraints**: Maintain all limitations from source specifications
- **Fidelity Agents**: Always use developer-fidelity and quality-reviewer-fidelity for implementation

### Code Simplification Workflow

1. Use `/simplify:create-plan` to analyze and plan
2. Quality review with @quality-reviewer agent
3. User approval required before implementation
4. Use `/simplify:process-plan` for execution

### Batch Documentation Workflow

Use `/docs:fetch-batch` to process multiple libraries from README sections:

1. **Markdown Parsing**: Extracts `[Library Name](URL)` patterns from bullet points
2. **Intelligent Mapping**: Maps display names to fetchable identifiers (e.g., "Next.js 15" → `nextjs --version 15`)
3. **Batch Processing**: Calls `/docs:fetch` for each library with appropriate parameters
4. **Progress Tracking**: Reports success/failure for each library in the batch
5. **CLAUDE.md Integration**: Automatically updates documentation references

Options:
- `--dry-run`: Preview what would be fetched
- `--parallel`: Process libraries concurrently (faster)
- `--skip-existing`: Skip libraries with existing documentation
- `--file README.md --section "Dependencies"`: Extract from file section

### Quality Standards

All agents reference CLAUDE.md for:

- Project-specific quality standards
- Error handling patterns
- Testing requirements
- Build and linting commands

When copying this repository setup to other projects, remember to recreate the .claude → .agents symlink structure.
