---
description: "Fetch and convert documentation for libraries, frameworks, and languages into AI-friendly Markdown format"
argument-hint: "[library_name] [--version VERSION] [--sections SECTIONS] [--update] [--format FORMAT] [--url URL]"
---

# Documentation Fetch Command

Fetch and curate documentation for programming libraries, frameworks, coding languages, and toolsets. This command transforms scattered online documentation into locally stored, AI-friendly Markdown files within the `/workspace/docs/` directory.

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

The AI should:

1. **Parse Arguments**: Extract library name and optional parameters from `$ARGUMENTS`.
2. **Source Discovery**: Identify official documentation URLs and site patterns (using the local `site-patterns.json` when helpful).
3. **Content Fetching**: Use the local helper script to fetch and convert docs:
   - Invoke `python codex/scripts/docs-fetch.py $ARGUMENTS` from the repository root.
4. **Content Processing**: Convert HTML to AI-friendly Markdown and organize sections logically for coding assistance.
5. **Storage**: Save results under `/workspace/docs/` (or the repo’s configured docs directory) with consistent naming.
6. **Repository Integration**: If `CLAUDE.md` or `README.md` describe local docs, update them briefly to mention the new docs location.
