---
description: "Fetch and convert documentation for libraries, frameworks, and languages into AI-friendly Markdown format"
argument-hint: "[library_name] [--version VERSION] [--sections SECTIONS] [--update] [--format FORMAT] [--url URL]"
---

# Documentation Fetch Command

Fetch and curate documentation for programming libraries, frameworks, coding languages, and toolsets. This command transforms scattered online documentation into locally stored, AI-friendly Markdown files within the `/workspace/docs/` directory. Think harder.

The package we are refering to will be provided via $ARGUMENTS

## Usage

```bash
/docs:fetch react                    # Fetch React documentation
/docs:fetch typescript --version 5.3 # Specific version
/docs:fetch lodash --sections api    # API reference only
/docs:fetch vue --update             # Update existing docs
/docs:fetch express --format minimal # Condensed format
/docs:fetch mylibrary --url https://docs.mylibrary.com/  # Manual URL
```

## Arguments

- **library_name** (required): Name of library/framework to fetch documentation for
- **--version** (optional): Specific version to fetch
- **--sections** (optional): Specific sections to fetch (api, guides, examples)
- **--update** (optional): Update existing documentation
- **--format** (optional): Output format (full, minimal, api-only)
- **--url** (optional): Manually specify documentation URL when auto-discovery fails

## Implementation

$ARGUMENTS

I'll help you fetch and curate documentation for the specified library or framework. Let me process your request:

1. **Parse Arguments**: Extract library name and optional parameters
2. **Source Discovery**: Identify official documentation URLs and site patterns
3. **Content Fetching**: Use appropriate scraping method based on site type
4. **Content Processing**: Convert HTML to AI-friendly Markdown format
5. **Organization**: Structure content using Technical Writer agent patterns
6. **Storage**: Save to `/workspace/docs/` with consistent naming conventions

Let me start by parsing your arguments and executing the documentation fetch process.

<function_calls>
<invoke name="Bash">
<parameter name="command">python .claude/scripts/docs-fetch.py $ARGUMENTS</parameter>
<parameter name="description">Execute documentation fetch script with user arguments</parameter>
</invoke>

Now let me update CLAUDE.md to reference the newly fetched documentation so Claude Code knows where to find it for future assistance.

<function_calls>
<invoke name="Edit">
<parameter name="file_path">CLAUDE.md</parameter>
<parameter name="old_string">## Repository Structure

This is a Claude Code configuration repository containing:

- **agents/**: Custom agent definitions for specialized tasks (developer, quality-reviewer, simplify-planner, etc.)
- **commands/**: Custom slash commands for task processing and code management
- **settings.json**: Claude Code configuration with custom status line and MCP servers</parameter>
  <parameter name="new_string">## Repository Structure

This is a Claude Code configuration repository containing:

- **agents/**: Custom agent definitions for specialized tasks (developer, quality-reviewer, simplify-planner, etc.)
- **commands/**: Custom slash commands for task processing and code management
- **docs/**: Fetched documentation for libraries, frameworks, and languages (AI-optimized Markdown format)
- **settings.json**: Claude Code configuration with custom status line and MCP servers</parameter>
  </invoke>

<function_calls>
<invoke name="Read">
<parameter name="file_path">CLAUDE.md</parameter>
<parameter name="offset">40</parameter>
<parameter name="limit">20</parameter>
</invoke>
