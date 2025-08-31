---
description: "Fetch and convert documentation for libraries, frameworks, and languages into AI-friendly Markdown format"
argument-hint: "[library_name] [--version VERSION] [--sections SECTIONS] [--update] [--format FORMAT]"
---

# Documentation Fetch Command

Fetch and curate documentation for programming libraries, frameworks, coding languages, and toolsets. This command transforms scattered online documentation into locally stored, AI-friendly Markdown files within the `/workspace/docs/` directory.

## Usage

```bash
/docs:fetch react                    # Fetch React documentation
/docs:fetch typescript --version 5.3 # Specific version
/docs:fetch lodash --sections api    # API reference only
/docs:fetch vue --update             # Update existing docs
/docs:fetch express --format minimal # Condensed format
```

## Arguments

- **library_name** (required): Name of library/framework to fetch documentation for
- **--version** (optional): Specific version to fetch
- **--sections** (optional): Specific sections to fetch (api, guides, examples)  
- **--update** (optional): Update existing documentation
- **--format** (optional): Output format (full, minimal, api-only)

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
<parameter name="command">cd /workspace && python scripts/docs-fetch.py $ARGUMENTS</parameter>
<parameter name="description">Execute documentation fetch script with user arguments</parameter>
</invoke>